import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize WebDriver
driver = webdriver.Chrome()

# URL to scrape
url = "https://www.baseball-reference.com/leagues/MLB.shtml"

# Open the webpage
driver.get(url)
time.sleep(5)  # Allow page to load

# Find the table element containing the stats
stat_table = driver.find_element(By.CLASS_NAME, 'stats_table')

# Extract player data (customize according to your table structure)
players = stat_table.find_elements(By.TAG_NAME, 'tr')

# Prepare your stats dictionary
stats = {
    "Batting Average": [],
    "On Base Percentage": [],
    "Slugging": [],
    "Home Runs": [],
    "Stolen Bases": [],
}

for player in players[1:]:  # Skip the header row
    cells = player.find_elements(By.TAG_NAME, 'td')
    if len(cells) > 1:  # Ensure it's a valid row with data
        player_name = cells[1].text
        batting_avg = cells[4].text
        on_base_percentage = cells[5].text
        slugging = cells[6].text
        home_runs = cells[8].text
        stolen_bases = cells[11].text

        # Add player data to the stats dictionary
        stats["Batting Average"].append({"name": player_name, "value": batting_avg})
        stats["On Base Percentage"].append({"name": player_name, "value": on_base_percentage})
        stats["Slugging"].append({"name": player_name, "value": slugging})
        stats["Home Runs"].append({"name": player_name, "value": home_runs})
        stats["Stolen Bases"].append({"name": player_name, "value": stolen_bases})

# Close the driver
driver.quit()

# Save or process the stats
print(stats)
