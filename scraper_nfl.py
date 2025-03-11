import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Create a temporary directory for user data to avoid conflicts
user_data_dir = tempfile.mkdtemp()

# Set up Chrome options to use the temporary user data directory
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Ensure a unique user data dir
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (necessary in headless mode)
chrome_options.add_argument("--no-sandbox")  # Avoid sandboxing issues in some environments

# Initialize WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the NFL Leaders page directly
leaders_url = "https://www.pro-football-reference.com/years/2024/leaders.htm"
driver.get(leaders_url)
print("Navigated to the NFL Leaders page.")

# Wait for the page to load completely
time.sleep(5)

# Define the IDs of the divs you want to scrape data from
div_ids = {
    "Passing Yds": "leaders_pass_yds",
    "Passing Touchdowns": "leaders_pass_td",
    "Passer Rating": "leaders_pass_rating",
    "Interceptions": "leaders_pass_int",
    "Rushing Yards": "leaders_rush_yds",
    "Rushing Touchdowns": "leaders_rush_td",
    "Rushing Yards per Attempt": "leaders_rush_yds_per_att",
    "Rushing Yards per Game": "leaders_rush_yds_per_g",
    "Receiptions": "leaders_rec",
    "Receiving Yards per Reception": "leaders_rec_yds_per_rec",
    "Receiving Yards per Game": "leaders_rec_yds_per_g",
    "Total Touchdowns": "leaders_all_td_no_other",
}

# Dictionary to store stats data
stats = {stat_name: [] for stat_name in div_ids.keys()}

# Scrape each stat from the corresponding div
for stat_name, div_id in div_ids.items():
    try:
        # Locate the div by ID
        stats_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, div_id))
        )
        print(f"Located the {stat_name} stats container by div ID: {div_id}")

        # Scroll into view BEFORE clicking button
        driver.execute_script("arguments[0].scrollIntoView();", stats_div)
        time.sleep(1)  # Allow scroll to finish

        # Look for a button inside the div and click it if present
        try:
            button = stats_div.find_element(By.TAG_NAME, "button")
            button.click()
            print(f"Clicked the button for {stat_name} to expand data.")
            time.sleep(2)  # Allow content to load
        except Exception:
            print(f"No button found for {stat_name}, continuing.")

        # Wait for the tbody to load completely
        tbody = WebDriverWait(stats_div, 5).until(
            EC.presence_of_element_located((By.TAG_NAME, 'tbody'))
        )

        # Ensure all rows have loaded before extracting
        WebDriverWait(tbody, 5).until(
            lambda d: len(tbody.find_elements(By.TAG_NAME, "tr")) >= 10
        )

        # Extract ALL rows within tbody
        rows = tbody.find_elements(By.TAG_NAME, "tr")

        print(f"Found {len(rows)} rows for {stat_name}")

        # Extract data for each row
        for row in rows:
            try:
                # Find all columns (td elements) in the row
                cells = row.find_elements(By.TAG_NAME, 'td')

                # Ensure the row has at least 3 columns (rank, player, stat)
                if len(cells) >= 3:
                    rank = cells[0].text.strip()
                    player_name = cells[1].text.strip()
                    stat_value = cells[2].text.strip()

                    # Add player data to the corresponding stat list in the dictionary
                    stats[stat_name].append({
                        "Rank": rank,
                        "Player": player_name,
                        stat_name: stat_value
                    })

            except Exception as e:
                print(f"Error processing row in {stat_name}: {e}")
                continue  # Skip problematic rows

    except Exception as e:
        print(f"Failed to find the stats div for {stat_name} with ID {div_id}: {e}")

# Close the driver after scraping
driver.quit()

# Debugging: Print extracted data
print("\nExtracted Stats:")
print(json.dumps(stats, indent=4))

# Save the stats dictionary to a JSON file
json_filename = 'nfl_leader_stats_table.json'

# Ensure data is collected before saving
if any(stats.values()):  # Check if at least one category contains data
    try:
        with open(json_filename, 'w') as json_file:
            json.dump(stats, json_file, indent=4)
        print(f"Stats have been saved to '{json_filename}'.")
    except Exception as e:
        print(f"Failed to save JSON file: {e}")
else:
    print("No data scraped. JSON file not created.")
