import sqlite3
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Database setup
db_name = "attendance_data.db"
table_name = "AttendanceHistory"

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
        # Convert date from MM/DD/YY to 'Month Day'
        return datetime.strptime(date, "%m/%d/%y").strftime("%B %-d")
    except ValueError as e:
        print(f"Date formatting error: {e}")
        return None

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

# Insert data into the database
def insert_data(year, date, attendance):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (year, date, attendance)
                VALUES (?, ?, ?)
            """, (year, date, attendance))
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate entry for {year} - {date}")
        conn.commit()

# Scrape attendance data for a specific year and date
def scrape_attendance(year, date):
    url = f"https://en.wikipedia.org/wiki/{year}_Michigan_State_Spartans_football_team"
    print(f"Fetching data from: {url}")
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch page for {year}. HTTP Status Code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all rows with the specific class 'CFB-schedule-row'
    rows = soup.find_all('tr', {'class': 'CFB-schedule-row'})

    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:  # Ensure the row has enough cells
            date_text = cells[0].get_text(strip=True)  # Date is in the first cell
            if date in date_text:  # Match the provided date
                try:
                    # Attendance is in the last cell
                    attendance = cells[-1].get_text(strip=True).replace(',', '')
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

    create_table()

    for date in dates:
        try:
            year = int(date.split('/')[-1]) + 2000  # Convert 2-digit year to 4-digit year
            formatted_date = convert_date_format(date)  # Convert to 'Month Day'

            if not formatted_date:
                print(f"Skipping invalid date format: {date}")
                continue

            attendance = scrape_attendance(year, formatted_date)
            if attendance is not None:
                print(f"Scraped: {year} - {formatted_date} - {attendance}")
                insert_data(year, formatted_date, attendance)
            else:
                print(f"No data for {formatted_date}")
        except Exception as e:
            print(f"Error processing date {date}: {e}")

    print(f"Data successfully imported into the '{table_name}' table in the '{db_name}' database.")

if __name__ == "__main__":
    main()
