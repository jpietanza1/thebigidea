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
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")  # Ensure a unique user data dir
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (necessary in headless mode)
chrome_options.add_argument("--no-sandbox")  # Avoid sandboxing issues in some environments

# Initialize WebDriver with the specified options
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Navigate to the webpage
url = "https://www.pro-football-reference.com/years/2024/fantasy.htm"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll and click on 'QBR' to sort
table_location = driver.find_element(By.ID, "fantasy")
driver.execute_script("arguments[0].scrollIntoView();", table_location)
time.sleep(2)
driver.execute_script("window.scrollBy(0, -200);")
time.sleep(2)

# Re-locate the table
table = driver.find_element(By.ID, "fantasy")

# Step 1: Dynamically build a map of column names to their indexes by checking if they contain the target text
header_cells = table.find_elements(By.XPATH, ".//thead/tr[2]/th")
column_indexes = {}
target_columns = ["Player", "FantPos", "PosRank"]

for idx, cell in enumerate(header_cells):
    header_text = cell.text.strip().lower()
    for target in target_columns:
        if target in header_text:
            column_indexes[target] = idx
            break  # Stop after finding the target column

# Step 2: Extract relevant data by those column indexes
data = []
for tr in table.find_elements(By.XPATH, ".//tbody/tr[not(contains(@class, 'thead'))]"):
    td_cells = tr.find_elements(By.TAG_NAME, "td")

    # Some rows may use <th> for the first column (e.g. Player)
    th_cells = tr.find_elements(By.TAG_NAME, "th")
    if th_cells:
        td_cells.insert(0, th_cells[0])

    if len(td_cells) >= max(column_indexes.values(), default=0) + 1:
        row_data = {}
        for col_name, index in column_indexes.items():
            row_data[col_name] = td_cells[index].text.strip()
        if row_data:
            data.append(row_data)

print(f"Total rows scraped: {len(data)}")

# Step 3: Refine data by position and save each position into its own file
positions = ['rb', 'qb', 'wr']  # The fantasy positions you want to separate

for position in positions:
    filtered_data = [player for player in data if player.get('fantpos', '').lower() == position]
    
    if filtered_data:
        with open(f"NFL_{position.upper()}_Players.json", "w", encoding="utf-8") as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        print(f"Data saved for {position.upper()} to {position.upper()}_Players.json")
    else:
        print(f"No data found for {position.upper()}.")

# Close browser
driver.quit()
