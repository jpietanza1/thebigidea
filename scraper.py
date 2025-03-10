import json
from selenium import webdriver

def scrape_mlb_stats():
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background
    driver = webdriver.Chrome(options=options)

    url = "https://www.baseball-reference.com/leagues/MLB.shtml"
    driver.get(url)
    
    # Example: Extract Batting Leaders
    leaders = driver.find_element("id", "leaders_batting_avg").text.split("\n")
    
    # Format data
    stats = {
        "Batting Average": [{"name": leaders[i], "value": leaders[i+1]} for i in range(0, len(leaders), 2)]
    }
    
    driver.quit()

    # Save as JSON
    with open("stats.json", "w") as f:
        json.dump(stats, f, indent=4)

if __name__ == "__main__":
    scrape_mlb_stats()
