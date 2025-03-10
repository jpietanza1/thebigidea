import requests
from bs4 import BeautifulSoup

def scrape_mlb_stats():
    url = "https://www.baseball-reference.com/leagues/MLB.shtml"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return {}

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the correct table
    stat_table = soup.find('table', {'id': 'league_batting'})  # ID is more reliable than class

    if not stat_table:
        print("Could not find the stats table. The website structure may have changed.")
        return {}

    rows = stat_table.find_all('tr')

    stats = {
        "Batting Average": [],
        "On Base Percentage": [],
        "Slugging": [],
        "Home Runs": [],
        "Stolen Bases": [],
    }

    for row in rows[1:]:
        cells = row.find_all('td')
        if len(cells) < 8:  # Adjusted to avoid IndexError
            continue
        
        player_name = cells[0].get_text(strip=True) if len(cells) > 0 else "N/A"
        batting_avg = cells[3].get_text(strip=True) if len(cells) > 3 else "N/A"
        on_base_percentage = cells[4].get_text(strip=True) if len(cells) > 4 else "N/A"
        slugging = cells[5].get_text(strip=True) if len(cells) > 5 else "N/A"
        home_runs = cells[8].get_text(strip=True) if len(cells) > 8 else "N/A"
        stolen_bases = cells[11].get_text(strip=True) if len(cells) > 11 else "N/A"

        stats["Batting Average"].append({"name": player_name, "value": batting_avg})
        stats["On Base Percentage"].append({"name": player_name, "value": on_base_percentage})
        stats["Slugging"].append({"name": player_name, "value": slugging})
        stats["Home Runs"].append({"name": player_name, "value": home_runs})
        stats["Stolen Bases"].append({"name": player_name, "value": stolen_bases})

    return stats

if __name__ == "__main__":
    stats = scrape_mlb_stats()
    print(stats)
