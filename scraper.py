import requests
from bs4 import BeautifulSoup

def scrape_mlb_stats():
    url = "https://www.baseball-reference.com/leagues/MLB.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table with player stats
    stat_table = soup.find('table', {'class': 'stats_table'})
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
        if len(cells) < 8:  # Skip rows with incomplete data
            continue
        player_name = cells[1].get_text()
        batting_avg = cells[4].get_text()
        on_base_percentage = cells[5].get_text()
        slugging = cells[6].get_text()
        home_runs = cells[8].get_text()
        stolen_bases = cells[11].get_text()

        stats["Batting Average"].append({"name": player_name, "value": batting_avg})
        stats["On Base Percentage"].append({"name": player_name, "value": on_base_percentage})
        stats["Slugging"].append({"name": player_name, "value": slugging})
        stats["Home Runs"].append({"name": player_name, "value": home_runs})
        stats["Stolen Bases"].append({"name": player_name, "value": stolen_bases})

    return stats

if __name__ == "__main__":
    stats = scrape_mlb_stats()
    print(stats)
