import sqlite3
import requests
from bs4 import BeautifulSoup

# Database setup
db_name = "attendance_data.db"
table_name = "AttendanceHistory"

# Read dates from the text file
def read_dates(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

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
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch page for {year}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table', class_='wikitable')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 1:
                date_text = cells[0].get_text(strip=True)  # Assume date is in the first column
                if date in date_text:  # Match the date
                    try:
                        attendance = cells[5].get_text(strip=True).replace(',', '')
                        return int(attendance)
                    except (IndexError, ValueError):
                        return None
    return None

# Main script execution
def main():
    dates_file = 'sport.txt'
    dates = read_dates(dates_file)
    create_table()

    for date in dates:
        year = int(date.split('/')[-1]) + 2000  # Convert 2-digit year to 4-digit year
        formatted_date = f"{date.split('/')[0]}/{date.split('/')[1]}/{str(year)}"  # Convert to MM/DD/YYYY
        attendance = scrape_attendance(year, date)
        if attendance is not None:
            print(f"Scraped: {year} - {formatted_date} - {attendance}")
            insert_data(year, formatted_date, attendance)

    print(f"Data successfully imported into the '{table_name}' table in the '{db_name}' database.")

if __name__ == "__main__":
    main()