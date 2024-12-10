import sqlite3
import matplotlib.pyplot as plt

# Database setup
db_name = "full_attendance_data.db"
output_file = "attendance_intervals.txt"

def calculate_attendance_intervals():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # Query to get all attendance values
        query = "SELECT attendance FROM AttendanceHistory"
        cursor.execute(query)
        attendance_data = [row[0] for row in cursor.fetchall()]
        
        # Define intervals up to 80,000-89,999
        interval_size = 10000
        max_interval = 80000
        intervals = list(range(0, max_interval + interval_size, interval_size))
        frequency = {f"{start}-{start + interval_size - 1}": 0 for start in intervals[:-1]}

        for attendance in attendance_data:
            for start in intervals[:-1]:
                if start <= attendance < start + interval_size:
                    frequency[f"{start}-{start + interval_size - 1}"] += 1
                    break
        
        # Write the results to a text file
        with open(output_file, 'w') as f:
            for interval, count in frequency.items():
                f.write(f"{interval}: {count} events\n")
        
        print(f"Attendance interval frequencies written to '{output_file}'.")

if __name__ == "__main__":
    calculate_attendance_intervals()

