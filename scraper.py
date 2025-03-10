from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# List of stats we want to scrape
STAT_CATEGORIES = ["Batting Average", "On-Base Percentage", "Slugging Percentage", "Home Runs", "Stolen Bases"]

def get_mlb_stats(stat_name):
    url = "https://www.baseball-reference.com/leagues/majors/2024-batting-leaders.shtml"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "leaders_standard_batting"})  # Main batting leaders table

    if not table:
        return []

    players = []
    headers = [th.text.strip() for th in table.find_all("th")]

    try:
        stat_index = headers.index(stat_name)
    except ValueError:
        return [{"error": f"Stat '{stat_name}' not found. Available: {headers[1:]}"}]

    for row in table.find_all("tr")[1:11]:  # Top 10 players
        cols = row.find_all("td")
        if len(cols) < stat_index:
            continue
        player_name = cols[0].text.strip()
        stat_value = cols[stat_index - 1].text.strip()
        players.append({"player": player_name, "stat": stat_value})

    return players

@app.route("/api/mlb-stats", methods=["GET"])
def mlb_stats():
    stat_name = request.args.get("stat", "Batting Average")
    data = get_mlb_stats(stat_name)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
