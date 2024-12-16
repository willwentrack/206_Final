import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Database paths
attendance_db = "full_attendance_data.db"
temperature_csv = "temperature_averages.csv" # end file to store in

conn = sqlite3.connect(attendance_db) # Connect to the attendance database


# Check if AttendanceHistory table exists from the attendance_db
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='AttendanceHistory';")
if not cursor.fetchone():
    raise ValueError("Table 'AttendanceHistory' does not exist in the database.")

cursor.execute("SELECT COUNT(*) FROM AttendanceHistory;")
if cursor.fetchone()[0] == 0:
    raise ValueError("Table 'AttendanceHistory' exists but contains no data.")

temperature_data = pd.read_csv(temperature_csv) # load in the data

temperature_data['Date'] = pd.to_datetime(temperature_data['Date'], errors='coerce') # this will make sure the date column is formated correctly

# Query to retrieve and format attendance data
query = """SELECT year, date, attendance FROM AttendanceHistory"""

attendance_data = pd.read_sql_query(query, conn)

# Make a unified date format (YYYY-MM-DD) for attendance data
attendance_data['formatted_date'] = pd.to_datetime(
    attendance_data['year'].astype(str) + " " + attendance_data['date'],
    format='%Y %B %d',
    errors='coerce'
)

# Merge datasets using the unified date format
merged_data = pd.merge(attendance_data, temperature_data, left_on="formatted_date", right_on="Date")

# Filter attendance to be within the range of 60,000 to 75,000
merged_data = merged_data[(merged_data['attendance'] >= 60000) & (merged_data['attendance'] <= 75000)]

# Make the data available for visualizing
if merged_data.empty:
    print("No data available to visualize.")
else:
    # Display the data
    print("Joined Data:")
    print(merged_data)

    # Calculate additional statistics
    avg_attendance = merged_data['attendance'].mean()
    max_attendance = merged_data['attendance'].max()
    min_attendance = merged_data['attendance'].min()
    avg_temperature = merged_data['Temp_Avg'].mean()

    print(f"Average Attendance: {avg_attendance:.2f}")
    print(f"Maximum Attendance: {max_attendance}") 
    print(f"Minimum Attendance: {min_attendance}")
    print(f"Average Temperature: {avg_temperature:.2f}\u00b0F")

    # Generate the plot
    plt.figure(figsize=(14, 8))

    # Attendance vs. Average Temperature
    plt.scatter(merged_data['Temp_Avg'], merged_data['attendance'], label="Data Points", alpha=0.8, edgecolors='k', c='skyblue', s=100)

    # Linear regression
    slope, intercept, r_value, p_value, std_err = linregress(merged_data['Temp_Avg'], merged_data['attendance'])
    line = slope * merged_data['Temp_Avg'] + intercept

    # Plot the line of fit
    plt.plot(merged_data['Temp_Avg'], line, color="red", linewidth=2, label=f"Line of Fit (r={r_value:.2f})")

    # Add gridlines
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Add titles and labels
    plt.title("MSU Attendance vs. Average Temperature", fontsize=16, fontweight='bold')
    plt.xlabel("Average Temperature (\u00b0F)", fontsize=14)
    plt.ylabel("Attendance", fontsize=14)

    # Customize ticks
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Add a legend with a border
    plt.legend(fontsize=12, frameon=True, loc='upper left', borderpad=1)

    # Annotate with additional stats
    stats_text = (f"Average Attendance: {avg_attendance:.2f}\n"
                  f"Max Attendance: {max_attendance}\n"
                  f"Min Attendance: {min_attendance}\n"
                  f"Avg Temperature: {avg_temperature:.2f}\u00b0F")
    plt.gcf().text(0.75, 0.2, stats_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

    # Save the graph as a PNG file
    output_file = "attendance_temp.png"
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Graph saved as {output_file}.")

    # Display the plot
    plt.show()

# Close the database connection
conn.close()
