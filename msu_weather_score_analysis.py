import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

# Database paths
msu_db = "msu_home_games.db"
weather_db = "weather_data.db"

# Connect to the MSU database and attach the Weather database
conn = sqlite3.connect(msu_db)
conn.execute(f"ATTACH DATABASE '{weather_db}' AS weather_db")

# Check if tables exist in both databases
cursor = conn.cursor()

# Check msu_home_games table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='msu_home_games';")
if not cursor.fetchone():
    raise ValueError("Table 'msu_home_games' does not exist in the database.")

cursor.execute("SELECT COUNT(*) FROM msu_home_games;")
if cursor.fetchone()[0] == 0:
    raise ValueError("Table 'msu_home_games' exists but contains no data.")

# Check FilteredWeatherHistory table
cursor.execute("SELECT name FROM weather_db.sqlite_master WHERE type='table' AND name='FilteredWeatherHistory';")
if not cursor.fetchone():
    raise ValueError("Table 'FilteredWeatherHistory' does not exist in the weather database.")

cursor.execute("SELECT COUNT(*) FROM weather_db.FilteredWeatherHistory;")
if cursor.fetchone()[0] == 0:
    raise ValueError("Table 'FilteredWeatherHistory' exists but contains no data.")

# Query to join data from both databases and calculate average temperature
query = """
SELECT 
    m.date, 
    m.msu_points, 
    (w.temp_max + w.temp_min) / 2.0 AS avg_temp
FROM 
    msu_home_games m
JOIN 
    weather_db.FilteredWeatherHistory w 
ON 
    m.date = w.date
ORDER BY 
    m.date;
"""

# Execute the query and fetch the data
joined_df = pd.read_sql_query(query, conn)

# Ensure the data is available for visualization
if joined_df.empty:
    print("No data available to visualize.")
else:
    # Display the data
    print("Joined Data:")
    print(joined_df)

    # Calculate additional statistics
    avg_points = joined_df['msu_points'].mean()
    max_points = joined_df['msu_points'].max()
    min_points = joined_df['msu_points'].min()
    avg_temperature = joined_df['avg_temp'].mean()

    print(f"Average MSU Points Scored: {avg_points:.2f}")
    print(f"Maximum MSU Points Scored: {max_points}")
    print(f"Minimum MSU Points Scored: {min_points}")
    print(f"Average Temperature: {avg_temperature:.2f}°C")

    # Generate the plot
    plt.figure(figsize=(14, 8))

    # Points vs. Average Temperature
    plt.scatter(joined_df['avg_temp'], joined_df['msu_points'], label="Data Points", alpha=0.8, edgecolors='k', c='skyblue', s=100)

    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(joined_df['avg_temp'], joined_df['msu_points'])
    line = slope * joined_df['avg_temp'] + intercept

    # Plot the line of fit
    plt.plot(joined_df['avg_temp'], line, color="red", linewidth=2, label=f"Line of Fit (r={r_value:.2f})")

    # Add gridlines
    plt.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Add titles and labels
    plt.title("MSU Points Scored vs. Average Temperature", fontsize=16, fontweight='bold')
    plt.xlabel("Average Temperature (°C)", fontsize=14)
    plt.ylabel("MSU Points Scored", fontsize=14)

    # Customize ticks
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Add a legend with a border
    plt.legend(fontsize=12, frameon=True, loc='upper left', borderpad=1)

    # Annotate with additional stats
    stats_text = (f"Average Points: {avg_points:.2f}\n"
                  f"Max Points: {max_points}\n"
                  f"Min Points: {min_points}\n"
                  f"Avg Temperature: {avg_temperature:.2f}°C")
    plt.gcf().text(0.75, 0.2, stats_text, fontsize=12, bbox=dict(facecolor='white', alpha=0.5))

    # Save the graph as a PNG file
    output_file = "msu_points_vs_avg_temperature_with_fit_fancy_stats.png"
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Graph saved as {output_file}.")

    # Display the plot
    plt.show()

# Close the database connection
conn.close()
