from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# List of stats we want to scrape
STAT_CATEGORIES = ["Batting Average", "On-Base Percentage", "Slugging Percentage", "Home Runs", "Stolen Bases"]

def get_mlb_stats():
    url = "https://www.baseball-reference.com/leagues/majors/2024-batting-leaders.shtml"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": "Failed to retrieve data"}

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "leaders_standard_batting"})  # Main batting leaders table

    if not table:
        return {"error": "Table not found"}

    stats_data = {stat: [] for stat in STAT_CATEGORIES}
    headers = [th.text.strip() for th in table.find_all("th")]

    for stat_name in STAT_CATEGORIES:
        try:
            stat_index = headers.index(stat_name)
        except ValueError:
            continue

        players = []
        for row in table.find_all("tr")[1:11]:  # Top 10 players
            cols = row.find_all("td")
            if len(cols) < stat_index:
                continue
            player_name = cols[0].text.strip()
            stat_value = cols[stat_index - 1].text.strip()
            players.append({"player": player_name, "value": stat_value})

        stats_data[stat_name] = players
    
    return stats_data

@app.route("/api/baseball-stats", methods=["GET"])
def baseball_stats():
    data = get_mlb_stats()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
