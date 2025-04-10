import time
import json
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Create a temporary directory for user data to avoid conflicts
user_data_dir = tempfile.mkdtemp()

# Set up Chrome options to use the temporary user data directory
chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the webpage
url = "https://www.pro-football-reference.com/years/2024/fantasy.htm"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll to the table
table_location = driver.find_element(By.ID, "fantasy")
driver.execute_script("arguments[0].scrollIntoView();", table_location)
time.sleep(2)
driver.execute_script("window.scrollBy(0, -200);")
time.sleep(2)

# Re-locate the table
table = driver.find_element(By.ID, "fantasy")

# Map column names to indexes
header_cells = table.find_elements(By.XPATH, ".//thead/tr[2]/th")
column_indexes = {}
target_columns = ["player", "fantpos", "posrank"]

for idx, cell in enumerate(header_cells):
    header_text = cell.text.strip().lower()
    for target in target_columns:
        if target in header_text:
            column_indexes[target] = idx
            break

# Extract and clean data
data = []
for tr in table.find_elements(By.XPATH, ".//tbody/tr[not(contains(@class, 'thead'))]"):
    td_cells = tr.find_elements(By.TAG_NAME, "td")
    th_cells = tr.find_elements(By.TAG_NAME, "th")
    if th_cells:
        td_cells.insert(0, th_cells[0])

    if len(td_cells) >= max(column_indexes.values(), default=0) + 1:
        row_data = {}
        for col_name, index in column_indexes.items():
            value = td_cells[index].text.strip()

            # Clean asterisks and plus signs from player names
            if col_name == "player":
                value = value.replace("*", "").replace("+", "")

            row_data[col_name] = value
        if row_data:
            data.append(row_data)

print(f"Total rows scraped: {len(data)}")

# Filter and save per position
positions = ['rb', 'qb', 'wr']

for position in positions:
    filtered_data = [player for player in data if player.get('fantpos', '').lower() == position]

    if filtered_data:
        with open(f"NFL_{position.upper()}_Players.json", "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved for {position.upper()} to NFL_{position.upper()}_Players.json")
    else:
        print(f"No data found for {position.upper()}.")

# Close browser
driver.quit()
