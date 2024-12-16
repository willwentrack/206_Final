import cfbd
import pandas as pd
import sqlite3
from datetime import datetime

# Set up the CFBD API client
configuration = cfbd.Configuration()
configuration.api_key['Authorization'] = 'u3N5YeQ4CFO09Gf4n8/V8QCHouOPUB1w9Ml6Y3CAGmfJIwgrAPMhn36F/dbH7C+L'
configuration.api_key_prefix['Authorization'] = 'Bearer'
api_config = cfbd.ApiClient(configuration)

# Initialize SQLite database
db_name = "msu_home_games1.db"
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Create only the msu_home_games table
cursor.execute("""
CREATE TABLE IF NOT EXISTS msu_home_games (
    game_id INTEGER PRIMARY KEY,
    date TEXT,
    opponent TEXT,
    msu_points INTEGER
)
""")
conn.commit()

# Function to count already existing records in the table
def count_existing_records():
    cursor.execute("SELECT COUNT(*) FROM msu_home_games")
    return cursor.fetchone()[0]

# Fetch and process game data for a range of years
games_api = cfbd.GamesApi(api_config)

def fetch_msu_home_games(start_year, end_year, max_records=25):
    existing_count = count_existing_records()  # Get the number of records already in the database
    target_count = existing_count + max_records  # Determine the target count after this run
    
    all_games = []  # Store all games for the entire range
    
    # Fetch all MSU games from start_year to end_year
    for year in range(start_year, end_year + 1):
        print(f"Fetching MSU home games for {year}...")
        games = games_api.get_games(year=year, team="Michigan State")
        for game in games:
            if game.home_team == "Michigan State":  # Filter for MSU home games
                formatted_date = datetime.strptime(game.start_date[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
                game_data = {
                    "game_id": game.id,
                    "date": formatted_date,
                    "opponent": game.away_team,
                    "msu_points": game.home_points
                }
                all_games.append(game_data)
    
    # Insert only the next 25 records based on existing count
    new_games = all_games[existing_count:target_count]  # Fetch the next 25 games
    for game in new_games:
        cursor.execute("""
        INSERT OR REPLACE INTO msu_home_games (game_id, date, opponent, msu_points)
        VALUES (:game_id, :date, :opponent, :msu_points)
        """, game)
    
    conn.commit()
    print(f"Inserted {len(new_games)} new records.")

# Fetch and store the next 25 MSU home games
fetch_msu_home_games(2009, 2023, max_records=25)

# Display the database content in descending order by date
print("MSU Home Games Data (Most Recent to Least Recent):")
df = pd.read_sql_query("SELECT * FROM msu_home_games ORDER BY date DESC", conn)
print(df)

# Close the database connection
conn.close()
print(f"Database saved as {db_name}.")
