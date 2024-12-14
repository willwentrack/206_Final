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


def create_visualization(df):
    # create four scatter plots to visualize the relationships
    # between weather conditions and game outcomes
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # plot 1: see if warmer weather brings more fans
    ax1.scatter(df['temp_max'], df['attendance'])
    ax1.set_xlabel('temperature (°c)')
    ax1.set_ylabel('attendance')
    ax1.set_title('temperature vs attendance')
    
    # plot 2: see if rain keeps fans away
    ax2.scatter(df['precipitation'], df['attendance'])
    ax2.set_xlabel('precipitation (mm)')
    ax2.set_ylabel('attendance')
    ax2.set_title('precipitation vs attendance')
    
    # plot 3: see if temperature affects scoring
    ax3.scatter(df['temp_max'], df['msu_points'])
    ax3.set_xlabel('temperature (°c)')
    ax3.set_ylabel('msu points scored')
    ax3.set_title('temperature vs points scored')
    
    # plot 4: see if rain affects scoring
    ax4.scatter(df['precipitation'], df['msu_points'])
    ax4.set_xlabel('precipitation (mm)')
    ax4.set_ylabel('msu points scored')
    ax4.set_title('precipitation vs points scored')
    
    plt.tight_layout()
    plt.savefig('weather_impact_analysis.png')
    plt.close()

def main():
    # running all our analysis steps in sequence
    df = load_and_merge_data()
    calculate_correlations(df)
    create_visualization(df)
    print("analysis complete! check correlation_results.txt and weather_impact_analysis.png")

if __name__ == "__main__":
    main()