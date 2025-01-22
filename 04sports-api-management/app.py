from flask import Flask, jsonify
import requests, os

app = Flask(__name__)

SERP_API_URL = os.getenv("SPORTS_API_URL")
SERP_API_KEY = os.getenv("SPORTS_API_KEY")

@app.route('/sports', methods=['GET'])
def get_nfl_schedule():
    try:
        params = {
            "engine": "google",
            "q": "nfl schedule",
            "api_key": SERP_API_KEY
        }
        response = requests.get(SERP_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        games = data.get("sports_results", {}).get("games", [])
        if not games:
            return jsonify({"message": "No NFL schedule found", "games": []}), 200

        formatted_games = []
        for game in games:
            teams = game.get("teams", [])
            if len(teams) == 2:
                away_team = teams[0].get("name", "Unknown")
                home_team = teams[1].get("name", "Unknown")
            else:
                away_team, home_team = "Unknown", "Unknown"
            game_info = {
                "away_team": away_team,
                "home_team":home_team,
                "venue": game.get("date", "Unknown"),
                "date": game.get("date", "Unknown"),
                "time": f"{game.get('time', 'Unknown')} ET" if game.get("time", "Unknown") != "Unknown" else "Unknown"
            }
                formatted_games.append(game_info)
            
            return jsonify({"message": "NFL schedule found", "games": formatted_games}), 200
        except Exception as e:
            return jsonify({"message": "An error occurred", "error": str(e)}), 500

if __name__ =='__main__':
    app.run(debug=True, port= 8080)
            
        