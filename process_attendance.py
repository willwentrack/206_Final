#importing needed libraries 
# sqlite3 for database operations, matplotlib for creating the attendance graph
import sqlite3
import matplotlib.pyplot as plt 

# setting the file names
# database file containing MSU football attendance data
db_name = "full_attendance_data.db"
# file containing calculated attendance ranges and frequencies
output_file = "attendance_intervals.txt"

def calculate_attendance_intervals():
    # connecting to the database !!
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        
        # fetching all the attendance records from database

        query = "SELECT attendance FROM AttendanceHistory"
        cursor.execute(query)
        attendance_data = [row[0] for row in cursor.fetchall()]

        # setting up attendance ranges by 10,000 person intervals
        interval_size = 10000
        max_interval = 80000
        intervals = list(range(0, max_interval + interval_size, interval_size))
         # creating dictionary to store count of games in each attendance range
        frequency = {f"{start}-{start + interval_size - 1}": 0 for start in intervals[:-1]}

        # counting the number of games in each attendance range
        for attendance in attendance_data:
            for start in intervals[:-1]:
                if start <= attendance < start + interval_size:
                    frequency[f"{start}-{start + interval_size - 1}"] += 1
                    break
        
        # saving attendance distribution to txt file

        with open(output_file, 'w') as f:
            for interval, count in frequency.items():
                f.write(f"{interval}: {count} events\n")
        
        print(f"Attendance interval frequencies written to '{output_file}'.")
        
        # creating the bar graph
        plt.figure(figsize=(12, 6))
        bars = plt.bar(range(len(frequency)), list(frequency.values()))

        # adding title and labels
        plt.title('MSU Football Game Attendance Distribution')
        plt.xlabel('Attendance Range')
        plt.ylabel('Number of Events')
        
        # x-axis labels (adding + rotating)  
        plt.xticks(range(len(frequency)), list(frequency.keys()), rotation=45)
        
        # adding value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')
        
        # adjusting the layout + saving
        plt.tight_layout()
        plt.savefig('attendance_distribution.png')
        plt.close()

# run!! 
if __name__ == "__main__":
    calculate_attendance_intervals()