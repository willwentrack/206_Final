import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def load_and_merge_data():
    # establish connections to all three database files we created
    weather_conn = sqlite3.connect('weather_data.db')
    games_conn = sqlite3.connect('msu_home_games.db')
    attendance_conn = sqlite3.connect('attendance_data.db')
    
    # get weather data (temperature and precipitation for each game)
    weather_df = pd.read_sql_query("""
        SELECT date, temp_max, temp_min, precipitation 
        FROM FilteredWeatherHistory
    """, weather_conn)
    
    # get msu's points scored for each game
    games_df = pd.read_sql_query("""
        SELECT date, msu_points 
        FROM msu_home_games
    """, games_conn)
    
    # get attendance numbers for each game
    attendance_df = pd.read_sql_query("""
        SELECT date, attendance 
        FROM AttendanceHistory
    """, attendance_conn)
    
    # combine all the data into one dataframe by matching game dates
    # this is equivalent to doing SQL JOIN operations
    merged_df = pd.merge(weather_df, games_df, on='date')
    merged_df = pd.merge(merged_df, attendance_df, on='date')
    
    return merged_df

def calculate_correlations(df):
    # calculate correlation coefficients and p-values
    # correlation of 1 = perfect positive relationship
    # correlation of -1 = perfect negative relationship
    # correlation of 0 = no relationship
    # p-value < 0.05 =  correlation is statistically significant
    
    # analyze how temperature affects attendance
    temp_attendance_corr = stats.pearsonr(df['temp_max'], df['attendance'])
    
    # analyze how rain affects attendance
    precip_attendance_corr = stats.pearsonr(df['precipitation'], df['attendance'])

    # analyze how temperature affects msu's scoring
    temp_points_corr = stats.pearsonr(df['temp_max'], df['msu_points'])
    
    # analyze how rain affects msu's scoring
    precip_points_corr = stats.pearsonr(df['precipitation'], df['msu_points'])
    
    # saving all results to a text file for the project report
    with open('correlation_results.txt', 'w') as f:
        f.write("weather impact analysis on msu football\n")
        f.write("=====================================\n\n")
        
        f.write("impact on attendance:\n")
        f.write(f"temperature vs attendance: r={temp_attendance_corr[0]:.3f}, p={temp_attendance_corr[1]:.3f}\n")
        f.write(f"precipitation vs attendance: r={precip_attendance_corr[0]:.3f}, p={precip_attendance_corr[1]:.3f}\n\n")
        
        f.write("impact on msu points scored:\n")
        f.write(f"temperature vs points: r={temp_points_corr[0]:.3f}, p={temp_points_corr[1]:.3f}\n")
        f.write(f"precipitation vs points: r={precip_points_corr[0]:.3f}, p={precip_points_corr[1]:.3f}\n")