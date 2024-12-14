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