import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("baseball.db")

# Read CSVs
stats_df = pd.read_csv("al_top25_stats_2015_2025.csv")
standings_df = pd.read_csv("al_standings_2015_2025.csv")

# Write to database
stats_df.to_sql("player_stats", conn, if_exists="replace", index=False)
standings_df.to_sql("standings", conn, if_exists="replace", index=False)

# Commit and close
conn.commit()
conn.close()

print("Database import complete.")
