
# American League Stats Dashboard (2015–2025)

🔗 **Live Demo:** https://your-streamlit-link.streamlit.app  

---

## Project Overview

This capstone project builds a complete data pipeline using web scraping, database management, and interactive visualization.

The project scrapes American League baseball data from Baseball Almanac (2015–2025), stores the data in a SQLite database, and presents insights through an interactive Streamlit dashboard.

---

## Project Components

### 1. Web Scraping Program (`web_scraping.py`)

- Selenium is used to scrape:
  - Top 25 Player Leaders (Home Runs(HR), Runs Batted In(RBI), and Stolen Bases(SB))
  - American League Team Standings

- Handles:
  - Dynamic content
  - Missing tags
  - Data cleaning

- Outputs:
  - `al_top25_stats_2015_2025.csv`
  - `al_standings_2015_2025.csv`

---

### 2. Database Import Program (`database_import.py`)

- SV files are imported into SQLite
- Tables are created:
  - `player_stats`
  - `standings`
- Corrected data types
- `if_exists="replace"` is used for reproducibility

---

### 3. Command Line Query Program (`query_program.py`)

- Allow dynamic filtering by:
  - Year
  - Stat Type (HR, RBI, SB)
  - Winning teams (> .500)
- Implement SQL JOIN between:
  - `player_stats`
  - `standings`
- Use parameterized queries for security
- Handle invalid user input gracefully

---

### 4. Interactive Dashboard (`dashboard.py`)

Built with **Streamlit** and **Plotly Express**.

Includes:

-  **Bar Chart**  
  Top 25 leaders for selected year and stat

-  **Scatter Plot**  
  Relationship between player performance and team win percentage

-  **Line Chart**  
  Trend of average stat leaders from 2015–2025

---

##  Technologies Used

- Python
- Selenium
- Pandas
- SQLite3
- Streamlit
- Plotly Express

---

##  Project Structure

capstone_project/
│
├── web_scraping.py
├── database_import.py
├── query_program.py
├── dashboard.py
├── baseball.db
├── al_top25_stats_2015_2025.csv
├── al_standings_2015_2025.csv
├── requirements.txt
└── README.md



---

## Installation & Setup



```bash

1. Clone the repository
git clone https://github.com/merimastarlit/baseball-project-CTD.git
cd capstone_project

### 1. Install Dependencies

pip install -r requirements.txt

## How to Run

### 1. Scrape Data

python3 web_scraping.py

### 2. Import to Database

python3 database_import.py

### 3. Run CLI Query Program

python3 query_program.py

### 4. Launch Dashboard

streamlit run dashboard.py

```

Key Insights:

- HR leaders often belong to teams with higher win percentages.

- Offensive performance trends fluctuate across seasons.

- Certain years show notable spikes in HR averages.

- Player performance and team success show measurable correlation.

Deployment:

The Streamlit dashboard is deployed publicly via Streamlit Cloud.

Access it here:

👉 https://your-streamlit-link.streamlit.a
