from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_mlb_stats():
    url = "https://www.baseball-reference.com/leagues/MLB.shtml"

    options = Options()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    service = Service("/usr/bin/chromedriver")  # For GitHub Actions
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(3)

    stats = {
        "Batting Average": [],
        "On Base Percentage": [],
        "Slugging": [],
        "Home Runs": [],
        "Stolen Bases": [],
    }

    try:
        table = driver.find_element(By.ID, "league_batting")
        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 12:
                continue
            
            player_name = cells[0].text
            batting_avg = cells[3].text
            obp = cells[4].text
            slugging = cells[5].text
            home_runs = cells[8].text
            stolen_bases = cells[11].text

            stats["Batting Average"].append(f"<tr><td>{player_name}</td><td>{batting_avg}</td></tr>")
            stats["On Base Percentage"].append(f"<tr><td>{player_name}</td><td>{obp}</td></tr>")
            stats["Slugging"].append(f"<tr><td>{player_name}</td><td>{slugging}</td></tr>")
            stats["Home Runs"].append(f"<tr><td>{player_name}</td><td>{home_runs}</td></tr>")
            stats["Stolen Bases"].append(f"<tr><td>{player_name}</td><td>{stolen_bases}</td></tr>")

    except Exception as e:
        print("Error:", e)

    driver.quit()
    return stats

def update_html(stats):
    with open("sports.html", "r", encoding="utf-8") as file:
        html = file.read()

    new_html = html

    for category, rows in stats.items():
        table_html = f"""
        <h3>{category}</h3>
        <table border="1">
            <tr><th>Player</th><th>Value</th></tr>
            {''.join(rows)}
        </table>
        """
        new_html = new_html.replace(f"<!-- {category} -->", table_html)

    with open("sports.html", "w", encoding="utf-8") as file:
        file.write(new_html)

if __name__ == "__main__":
    stats = scrape_mlb_stats()
    update_html(stats)
    print("sports.html updated with new MLB stats!")
