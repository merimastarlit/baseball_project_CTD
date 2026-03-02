import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(page_title="AL Stats Dashboard", layout="wide")

st.title("American League Stats Dashboard (2015–2025)")

st.markdown("""
This dashboard explores American League Top 25 offensive leaders 
from 2015–2025 and analyzes the relationship between player performance 
and team success.
""")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
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
    return df

df = load_data()

# -----------------------------
# Filters Section
# -----------------------------
st.markdown("### Filters")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    year_selected = st.selectbox(
        "Select Year",
        sorted(df["year"].unique())
    )

with col_filter2:
    stat_selected = st.selectbox(
        "Select Stat",
        sorted(df["stat_type"].unique())
    )

winning_only = st.checkbox("Show only teams above .500")

# -----------------------------
# Filter Data
# -----------------------------
filtered_df = df[
    (df["year"] == year_selected) &
    (df["stat_type"] == stat_selected)
]

if winning_only:
    filtered_df = filtered_df[filtered_df["win_pct"] > 0.500]

# -----------------------------
# Create Visualizations
# -----------------------------

# Bar Chart
fig1 = px.bar(
    filtered_df.sort_values("value", ascending=False),
    x="player",
    y="value",
    title=f"Top 25 {stat_selected} Leaders in {year_selected}",
    labels={"value": stat_selected, "player": "Player"},
)

# Scatter Plot
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

# Line Chart (Trend Over Time)
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
    labels={"value": f"Average {stat_selected}", "year": "Year"}
)

# -----------------------------
# Layout Charts
# -----------------------------

st.markdown("### Player Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Historical Trend")

st.plotly_chart(fig3, use_container_width=True)