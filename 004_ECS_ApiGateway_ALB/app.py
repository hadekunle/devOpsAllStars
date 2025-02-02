from flask import Flask, jsonify, render_template_string, request
 
app = Flask(__name__)

# Mocked JSON response data
data = {
    "sports_results": {
        "game_spotlight": {
            "league": "NFL",
            "stadium": "Caesars Superdome",
            "stage": "Super Bowl",
            "date": "Sun, Feb 9, 6:30 PM",
            "teams": [
                {
                    "name": "Kansas City Chiefs",
                    "thumbnail": "https://ssl.gstatic.com/onebox/media/sports/logos/5N0l1KbG1BHPyP8_S7SOXg_96x96.png",
                },
                {
                    "name": "Philadelphia Eagles",
                    "thumbnail": "https://ssl.gstatic.com/onebox/media/sports/logos/s4ab0JjXpDOespDSf9Z14Q_96x96.png",
                },
            ],
            "venue": "Caesars Superdome"
        }
    }
}

# In-memory storage
votes = {"Kansas City Chiefs": 20, "Philadelphia Eagles": 3}
voters = {}  # Maps client_ip -> team they've voted for

@app.route("/", methods=["GET"])
def display_matchup():
    # Extract team information
    game_spotlight = data.get("sports_results", {}).get("game_spotlight", {})
    teams = game_spotlight.get("teams", [])
    team1 = teams[0] if len(teams) > 0 else {}
    team2 = teams[1] if len(teams) > 1 else {}

    # Render HTML
    html_template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SUPERBOWL FINALS</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f3f4f6;
            }
            .container {
                margin: 50px auto;
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                width: 80%;
                max-width: 600px;
            }
            h1 {
                margin-top: 0;
                padding-top: 20px;
            }
            .team {
                display: flex;
                align-items: center;
                justify-content: space-between;
                margin: 20px 0;
            }
            .team img {
                width: 60px;
                height: 60px;
                border-radius: 50%;
            }
            .vs {
                font-size: 24px;
                font-weight: bold;
                margin: 20px 0;
            }
            .venue {
                font-size: 16px;
                color: #555;
            }
            .vote-btn {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 10px;
            }
            .vote-btn:hover {
                background-color: #0056b3;
            }
            .votes {
                font-size: 18px;
                margin: 10px 0;
            }
        </style>
        <script>
            async function voteForTeam(teamName) {
                const response = await fetch('/vote', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ team: teamName }),
                });
                
                const data = await response.json();
                alert(data.message);
                
                // Update vote counts on page
                document.getElementById('votes').innerText = 
                    `Kansas City Chiefs: ${data.votes['Kansas City Chiefs']} | Philadelphia Eagles: ${data.votes['Philadelphia Eagles']}`;
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>SUPERBOWL FINALS</h1>
            <div class="team">
                <img src="{{ team1.get('thumbnail', '') }}" alt="{{ team1.get('name', '') }}">
                <span>{{ team1.get('name', 'Unknown Team') }}</span>
            </div>
            <div class="vs">VS</div>
            <div class="team">
                <img src="{{ team2.get('thumbnail', '') }}" alt="{{ team2.get('name', '') }}">
                <span>{{ team2.get('name', 'Unknown Team') }}</span>
            </div>
            <div class="venue">
                Venue: {{ game_spotlight.get('venue', 'Unknown') }} <br>
                Date: {{ game_spotlight.get('date', 'Unknown') }}
            </div>
            <div>
                <button class="vote-btn" onclick="voteForTeam('{{ team1.get('name', '') }}')">Vote for {{ team1.get('name', 'Team 1') }}</button>
                <button class="vote-btn" onclick="voteForTeam('{{ team2.get('name', '') }}')">Vote for {{ team2.get('name', 'Team 2') }}</button>
            </div>
            <div class="votes" id="votes">
                Kansas City Chiefs: {{ votes['Kansas City Chiefs'] }} | Philadelphia Eagles: {{ votes['Philadelphia Eagles'] }}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(
        html_template,
        team1=team1,
        team2=team2,
        game_spotlight=game_spotlight,
        votes=votes,
    )

@app.route("/vote", methods=["POST"])
def vote():
    global votes, voters
    client_ip = request.remote_addr  # Get the client's IP address
    team = request.json.get("team")

    # Validate team
    if team not in votes:
        return jsonify({"message": "Invalid team name.", "votes": votes}), 400

    previous_team = voters.get(client_ip)

    # If user has never voted before
    if previous_team is None:
        votes[team] += 1
        voters[client_ip] = team
        return jsonify({"message": "Vote counted!", "votes": votes})

    # If user is toggling off the same team
    if previous_team == team:
        votes[team] -= 1
        # Remove the user's vote record
        del voters[client_ip]
        return jsonify({"message": "Vote removed!", "votes": votes})

    # If user is switching from one team to another
    votes[previous_team] -= 1
    votes[team] += 1
    voters[client_ip] = team
    return jsonify({"message": f"Switched vote to {team}!", "votes": votes})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080,debug=True)
