import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Set up Streamlit app and title:
st.title("American League Stats Dashboard (2015–2025)")

# Connect to database
conn = sqlite3.connect("baseball.db")

query = """
SELECT 
    player_stats.year,
    player_stats.player,
    player_stats.stat_type,
    player_stats.value,
    player_stats.team,
    standings.win_pct
FROM player_stats
LEFT JOIN standings
    ON player_stats.year = standings.year
    AND player_stats.team = standings.team
"""

df = pd.read_sql(query, conn)
conn.close()

# Dropdown menus for year and stat type
year_selected = st.selectbox(
    "Select Year",
    sorted(df["year"].unique())
)

stat_selected = st.selectbox(
    "Select Stat",
    df["stat_type"].unique()
)


# Filter DataFrame based on selections
filtered_df = df[
    (df["year"] == year_selected) &
    (df["stat_type"] == stat_selected)
]


# Bar chart of top 25 players
fig1 = px.bar(
    filtered_df.sort_values("value", ascending=False),
    x="player",
    y="value",
    title=f"Top 25 {stat_selected} Leaders in {year_selected}",
)

st.plotly_chart(fig1)


# Scatter plot of player stat vs team win percentage
st.subheader("Relationship Between Player Performance and Team Success")

fig2 = px.scatter(
    filtered_df,
    x="value",
    y="win_pct",
    hover_name="player",
    title=f"{stat_selected} vs Team Win % ({year_selected})",
    labels={
        "value": stat_selected,
        "win_pct": "Win Percentage"
    }
)

st.plotly_chart(fig2)


# Line chart of average stat value over years
st.subheader("Trend of Average Stat Value Over Time")

trend_df = df[df["stat_type"] == stat_selected] \
    .groupby("year")["value"] \
    .mean() \
    .reset_index()

fig3 = px.line(
    trend_df,
    x="year",
    y="value",
    markers=True,
    title=f"Average {stat_selected} Leaders Value (2015–2025)",
    labels={"value": f"Average {stat_selected}"}
)

st.plotly_chart(fig3)