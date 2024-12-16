import sqlite3
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Database setup
db_name = "full_attendance_data.db"
table_name = "AttendanceHistory"

# Limit for entries per run
MAX_ENTRIES_PER_RUN = 25 # only 25 datapoints per run

# Read dates from the text file
def read_dates(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []

# Convert date format to match Wikipedia (e.g., September 1)
def convert_date_format(date):
    try:
        return datetime.strptime(date, "%m/%d/%y").strftime("%B %-d")
    except ValueError as e:
        print(f"Date formatting error: {e}")
        return None

# Normalize date from Wikipedia format to 'Month Day'
def normalize_date(date_text):
    try:
        return datetime.strptime(date_text, "%B %d").strftime("%B %-d")
    except ValueError:
        return date_text

# Create the database table
def create_table():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                year INTEGER,
                date TEXT,
                attendance INTEGER,
                PRIMARY KEY (year, date)
            )
        """)
        conn.commit()

# Check if a date already exists in the database
def is_date_in_db(year, date):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM {table_name} WHERE year = ? AND date = ?", (year, date))
        return cursor.fetchone() is not None

# Insert data into the database
def insert_data(year, date, attendance):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (year, date, attendance)
                VALUES (?, ?, ?)
            """, (year, date, attendance))
            conn.commit()
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate entry for {year} - {date}")

def scrape_special_years(year, date): # Scrape attendance data for special years (2009, 2011, 2012)
    url = f"https://en.wikipedia.org/wiki/{year}_Michigan_State_Spartans_football_team"
    print(f"Fetching data from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page for {year}. HTTP Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', {'class': 'wikitable'})

    if year == 2012:
        target_table = tables[3] if len(tables) >= 4 else None
    elif year in {2009, 2011}:
        # use the special year web-scraping format
        target_table = next((t for t in tables if 'Attendance' in [th.get_text(strip=True) for th in t.find('tr').find_all('th')]), None)
    else:
        return None

    if not target_table:
        print(f"No valid table found for {year}")
        return None

    rows = target_table.find_all('tr') 
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            raw_date_text = cells[0].get_text(strip=True)
            normalized_date = normalize_date(raw_date_text)
            if date == normalized_date:
                try:
                    attendance = cells[-1].get_text(strip=True)
                    attendance = re.sub(r"[^0-9]", "", attendance)
                    if len(attendance) > 5:
                        attendance = attendance[:5]
                    return int(attendance)
                except ValueError:
                    print(f"Error parsing attendance for {date} on {url}")
                    return None

    print(f"No attendance data found for {date} on {url}")
    return None

def scrape_attendance(year, date): # scrape for the normal years
    url = f"https://en.wikipedia.org/wiki/{year}_Michigan_State_Spartans_football_team"
    print(f"Fetching data from: {url}")
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page for {year}. HTTP Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser') # this is the format for the normal scrape years
    rows = soup.find_all('tr', {'class': 'CFB-schedule-row'})
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            raw_date_text = cells[0].get_text(strip=True)
            normalized_date = normalize_date(raw_date_text)
            if date == normalized_date:
                try:
                    attendance = cells[-1].get_text(strip=True)
                    attendance = re.sub(r"[^0-9]", "", attendance)
                    return int(attendance)
                except ValueError:
                    print(f"Error parsing attendance for {date} on {url}")
                    return None

    print(f"No attendance data found for {date} on {url}")
    return None

# Main script execution
def main():
    dates_file = 'sport.txt'
    dates = read_dates(dates_file)
    if not dates:
        print("No dates to process. Exiting.")
        return

    create_table() # make the table

    special_years = {2009, 2011, 2012} # initialize what years are special
    entries_added = 0

    for date in dates:
        if entries_added >= MAX_ENTRIES_PER_RUN: # if the entries exceed the max_entries
            print(f"Reached the limit of {MAX_ENTRIES_PER_RUN} entries for this run. Exiting.")
            break

        try:
            year_suffix = int(date.split('/')[-1])
            year = 2000 + year_suffix if year_suffix < 100 else year_suffix
            formatted_date = convert_date_format(date)

            if not formatted_date:
                print(f"Skipping invalid date format: {date}")
                continue

            if is_date_in_db(year, formatted_date):
                print(f"Skipping already stored date: {formatted_date} ({year})")
                continue

            if year in special_years:
                attendance = scrape_special_years(year, formatted_date)
            else:
                attendance = scrape_attendance(year, formatted_date)

            if attendance is not None:
                print(f"Scraped: {year} - {formatted_date} - {attendance}")
                insert_data(year, formatted_date, attendance)
                entries_added += 1
            else:
                print(f"No data for {formatted_date}")
        except Exception as e:
            print(f"Error processing date {date}: {e}")

    print(f"Added {entries_added} entries to the '{table_name}' table in the '{db_name}' database.")

if __name__ == "__main__":
    main()
