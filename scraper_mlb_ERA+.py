import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to the webpage
url = "https://www.baseball-reference.com/leagues/majors/2025-standard-pitching.shtml"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Scroll and click on 'Rbat+' to sort
table_location = driver.find_element(By.ID, "players_standard_pitching")
driver.execute_script("arguments[0].scrollIntoView();", table_location)
time.sleep(2)
driver.execute_script("window.scrollBy(0, -200);")
time.sleep(2)

# Sort by Rbat+
try:
    driver.find_element(By.CSS_SELECTOR, 'th[aria-label="ERA+"]').click()
    time.sleep(3)
except Exception as e:
    print("Could not click ERA+ header:", e)

# Re-locate the table
table = driver.find_element(By.ID, "players_standard_pitching")

# Extract only the first two columns from table rows
data = []
for tr in table.find_elements(By.XPATH, ".//tbody/tr[not(contains(@class, 'thead'))]"):
    th = tr.find_elements(By.TAG_NAME, "th")  # First column (usually Rank)
    td = tr.find_elements(By.TAG_NAME, "td")  # Rest of the row

    if th and len(td) >= 1:
        col1 = th[0].text  # First column
        col2 = td[0].text  # Second column
        data.append({"Column1": col1, "Column2": col2})

print(f"Total rows scraped: {len(data)}")

# Save to JSON
if data:
    df = pd.DataFrame(data)
    df.to_json("MLB_pitcher_ERA+.json", orient="records", indent=2)
    print("Data saved to MLB_pitcher_ERA+.json")
else:
    print("No data found.")
