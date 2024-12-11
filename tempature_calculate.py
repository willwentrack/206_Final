import sqlite3
import csv

# Database and table configuration
db_name = "weather_data.db"
table_name = "FilteredWeatherHistory"
output_csv = "temperature_averages.csv"

def calculate_temp_averages():
    """Calculates average temperature for all dates and saves to a CSV file."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            
            # Query to get all date, temp_max, and temp_min
            query = f"SELECT date, temp_max, temp_min FROM {table_name}"
            cursor.execute(query)
            records = cursor.fetchall()
            
            if not records:
                print("No data found in the database.")
                return
            
            # Calculate average temperature and round to 2 decimal places
            temp_data = [
                {"date": date, "temp_avg": round((temp_max + temp_min) / 2, 2)} 
                for date, temp_max, temp_min in records
            ]
            
            # Save to CSV
            with open(output_csv, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Date", "Temp_Avg"])
                for entry in temp_data:
                    csv_writer.writerow([entry["date"], entry["temp_avg"]])
            
            print(f"Average temperatures have been saved to '{output_csv}'.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    calculate_temp_averages()
