from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd


# driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=Options())

# helpful function copied from here:
# https://gist.github.com/toma63/c776e8f0913a656d551e0119fc7858a7
# lots more helpful selenium in that gist

# set up our browser
def setup_driver(headless=False):
    """Setup Chrome WebDriver with options"""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    return driver


# set up our browser
# use headless if running in production!
# driver = setup_driver(headless=True)


# Stats scraping
stats = ["HR", "RBI", "SB"]

# Mapping for display names
stat_map = {
    "HR": "Home Runs",
    "RBI": "Runs Batted In",
    "SB": "Stolen Bases"
}

# Initializing driver
driver = setup_driver()

# Collecting stats data
all_rows = []

# Loop through years and stats through the URLs
for year in range(2015, 2026):
    for stat in stats:
        url = f"https://www.baseball-almanac.com/yearly/top25.php?s={stat}&l=AL&y={year}"
        # Navigate to the page
        driver.get(url)

        #save the stat display name
        display_name = stat_map[stat]
        # checking if the urls are working
        print(url)

        # Wait for the table to load
        wait = WebDriverWait(driver, 10)

        #locating the table by finding the header first by display name
        wait.until(EC.presence_of_element_located(
            (By.XPATH, f'//h2[contains(text(), "{display_name}")]')))
        
        # Extracting table rows
        table = driver.find_element(
            By.XPATH, f'//h2[contains(text(), "{display_name}")]/following::table[1]')
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows: # go through each row
            # finding the cells and saving the data
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) == 4:
                player = cells[1].text.strip()
                value = cells[2].text.strip()
                team = cells[3].text.strip()

                # once we have the data, append to all_rows
                all_rows.append({
                    "year": year,
                    "stat_type": stat,
                    "player": player,
                    "value": value,
                    "team": team
                })

# Creating DataFrame
df = pd.DataFrame(all_rows)

# Cleaning 'value' column
df['value'] = pd.to_numeric(df['value'], errors="coerce")
df.dropna(subset=['value'], inplace=True)

# Save to CSV
df.to_csv("al_top25_stats_2015_2025.csv", index=False)  #

# Checking results
print(len(df))

print(df.head())
print(df['stat_type'].unique())
print(df['year'].unique())


# Standings scraping, the second table

# empty list to hold all standings data
all_standings = []

# Loop through years to get standings
for year in range(2015, 2026):

    # Construct URL for the year's standings
    yearly_url = f"https://www.baseball-almanac.com/yearly/yr{year}a.shtml"

    # Navigate to the page
    driver.get(yearly_url)

    # Wait for the table to load
    wait = WebDriverWait(driver, 10)

    # Locate the standings table by finding a banner class
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//td[contains(@class,'banner')]"))
    )
    # Extracting table rows
    rows = driver.find_elements(By.TAG_NAME, "tr")

    current_division = None

    for row in rows:
        # finding the cells in each row
        cells = row.find_elements(By.TAG_NAME, "td")

        if not cells:
            continue
        
        # checking the class of the first cell to determine row type
        first_cell_class = cells[0].get_attribute("class")

        # defining the division header row and saving it to current_division
        if first_cell_class and "banner" in first_cell_class:
            current_division = cells[0].text.strip()

        # defining the data rows and extracting the data
        elif first_cell_class and "datacolBox" in first_cell_class:
            if len(cells) >= 5:
                team = cells[0].text.strip().replace(" wc", "")
                wins = cells[1].text.strip()
                losses = cells[2].text.strip()
                wp = cells[4].text.strip()

                # appending the data to all_standings
                all_standings.append({
                    "year": year,
                    "division": current_division,
                    "team": team,
                    "wins": wins,
                    "losses": losses,
                    "win_pct": wp
                })

# Closing the driver after scraping
driver.quit()

# Checking results
print(len(all_standings))

# Creating DataFrame
standings_df = pd.DataFrame(all_standings)

print(standings_df.columns)
print(len(standings_df))
print(standings_df.head())

# Cleaning numeric columns
standings_df["wins"] = pd.to_numeric(standings_df["wins"], errors="coerce")
standings_df["losses"] = pd.to_numeric(standings_df["losses"], errors="coerce")
standings_df["win_pct"] = pd.to_numeric(
    standings_df["win_pct"], errors="coerce")

# Dropping rows with NaN values in numeric columns
standings_df.dropna(inplace=True)

# Save to CSV
standings_df.to_csv("al_standings_2015_2025.csv", index=False)

# Checking cleaned results
print(len(standings_df))
print(standings_df.head())
