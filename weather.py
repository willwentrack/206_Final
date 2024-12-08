import sqlite3
import urllib.request
import json
import sys

# List of specific dates to store
dates_to_store = [
    "2009-09-05", "2009-09-12", "2009-10-03", "2009-10-17", "2009-10-24", "2009-11-07", 
    "2009-11-21", "2010-09-04", "2010-09-18", "2010-09-25", "2010-10-02", "2010-10-16", 
    "2010-11-06", "2010-11-20", "2011-09-02", "2011-09-10", "2011-09-24", "2011-10-15", 
    "2011-10-22", "2011-11-05", "2011-11-19", "2012-08-31", "2012-09-15", "2012-09-22",
    "2012-09-29", "2012-10-13", "2012-11-03", "2012-11-17", "2013-08-30", "2013-09-07", 
    "2013-09-14", "2013-10-12", "2013-10-19", "2013-11-02", "2013-11-30", "2014-08-29", 
    "2014-09-20", "2014-09-27", "2014-10-04", "2014-10-25", "2014-11-08", "2014-11-22",
    "2015-09-12", "2015-09-19", "2015-09-26", "2015-10-03", "2015-10-24", "2015-11-14",
    "2015-11-28", "2016-09-02", "2016-09-24", "2016-10-08", "2016-10-15", "2016-10-22", 
    "2016-10-29", "2016-11-12", "2016-11-19", "2017-09-02", "2017-09-09", "2017-09-23",
    "2017-09-30", "2017-10-21", "2017-11-04", "2017-11-18", "2018-08-31", "2018-09-29", 
    "2018-10-06", "2018-10-20", "2018-10-27", "2018-11-10", "2018-11-24", "2019-08-30", 
    "2019-09-07", "2019-09-14", "2019-09-28", "2019-10-26", "2019-11-09", "2019-11-30",
    "2020-10-24", "2020-11-07", "2020-11-14", "2020-11-28", "2021-09-11", "2021-09-18", 
    "2021-09-25", "2021-10-02", "2021-10-30", "2021-11-13", "2021-11-27", "2022-09-02", 
    "2022-09-10", "2022-09-24", "2022-10-01", "2022-10-08", "2022-10-15", "2022-11-12", 
    "2022-11-19", "2023-09-01", "2023-09-09", "2023-09-16", "2023-09-23", "2023-10-21", 
    "2023-11-04", "2023-11-24"
]

# Database setup
db_name = "weather_data.db"
table_name = "FilteredWeatherHistory"

# Function to create the database table
def create_table():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                date TEXT PRIMARY KEY,
                temp_max REAL,
                temp_min REAL,
                precipitation REAL,
                description TEXT
            )
        """)
        conn.commit()

# Function to insert data into the database
def insert_data(day):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"""
                INSERT INTO {table_name} (date, temp_max, temp_min, precipitation, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                day.get("datetime"),
                day.get("tempmax"),
                day.get("tempmin"),
                day.get("precip"),
                day.get("description", "N/A")
            ))
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate entry for date: {day.get('datetime')}")
        conn.commit()

# Fetch data for each date
def fetch_data_for_date(date):
    try:
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/East%20Lansing/{date}/{date}?unitGroup=metric&key=YG3BWARZ7M7W7TADTU38X6J53&contentType=json"
        response = urllib.request.urlopen(url)
        json_data = json.load(response)
        if "days" in json_data and len(json_data["days"]) > 0:
            return json_data["days"][0]  # Return the first (and only) day's data
        else:
            print(f"No data found for date: {date}")
            return None
    except urllib.error.HTTPError as e:
        error_info = e.read().decode()
        print(f"HTTP Error for date {date}: {e.code} {error_info}")
        return None
    except urllib.error.URLError as e:
        print(f"URL Error for date {date}: {e.reason}")
        return None

# Main script execution
create_table()

for date in dates_to_store:
    day_data = fetch_data_for_date(date)  # Use the original date format directly
    if day_data:
        insert_data(day_data)

print(f"Data for specified dates successfully imported into the '{table_name}' table in the '{db_name}' database.")
