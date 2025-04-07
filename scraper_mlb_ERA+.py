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

# Navigate to the webpage
url = "https://www.baseball-reference.com/leagues/majors/2025-standard-pitching.shtml"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll and click on 'ERA+' to sort
table_location = driver.find_element(By.ID, "players_standard_pitching")
driver.execute_script("arguments[0].scrollIntoView();", table_location)
time.sleep(2)
driver.execute_script("window.scrollBy(0, -200);")
time.sleep(2)

# Sort by Rbat+ using WebDriverWait
try:
    # Wait until the 'ERA+' header is clickable
    era_header = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'th[aria-label="ERA+"]'))
    )
    era_header.click()
    time.sleep(2)  # Wait for sort to apply

    # Optional: Click again if you want to ensure descending order
    # era_header.click()
    # time.sleep(2)
except Exception as e:
    print("Could not click ERA+ header:", e)

# Re-locate the table
table = driver.find_element(By.ID, "players_standard_pitching")

# Extract only the first two columns from table rows
data = []
for tr in table.find_elements(By.XPATH, ".//tbody/tr[not(contains(@class, 'thead'))]"):
    th = tr.find_elements(By.TAG_NAME, "th")  # First column (usually Rank or Player)
    td = tr.find_elements(By.TAG_NAME, "td")  # Rest of the row

    if th and len(td) >= 1:
        col1 = th[0].text.strip()  # First column
        col2 = td[0].text.strip()  # Second column
        data.append({"Column1": col1, "Column2": col2})

print(f"Total rows scraped: {len(data)}")

# Save to JSON without pandas
if data:
    with open("MLB_pitcher_ERA+.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Data saved to MLB_pitcher_ERA_plus.json")
else:
    print("No data found.")

# Close browser
driver.quit()
