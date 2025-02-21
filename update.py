import requests
from datetime import datetime, timedelta
import pytz

utc_now = datetime.utcnow()
utc_zone = pytz.utc
est_zone = pytz.timezone('America/New_York')
utc_now = utc_zone.localize(utc_now)
est_time = utc_now.astimezone(est_zone)
date = (est_time - timedelta(days=1)).strftime('%Y-%m-%d')
est = est_time.strftime('%Y-%m-%d %H:%M:%S %Z')

url = f"https://api.sportsdata.io/v3/mlb/scores/json/ScoresBasic/{date}"
api_key = "86f6d790e07d4c4cacddef80790bec22"  # Keep API keys private!

headers = {"Ocp-Apim-Subscription-Key": api_key}  # Some APIs require headers

response = requests.get(url, headers=headers)

games = response.json()
for game in games:
    if game['AwayTeam'] == 'LAD' or game['HomeTeam'] == 'LAD':
        if game['AwayTeam'] == 'LAD':
            away_runs = game['AwayTeamRuns']
            home_runs = game['HomeTeamRuns']
            if away_runs > home_runs:
                result_text = 'yep'
            else:
                result_text = 'nope'
        if game['HomeTeam'] == 'LAD':
            away_runs = game['AwayTeamRuns']
            home_runs = game['HomeTeamRuns']
            if home_runs > away_runs:
                result_text = 'yep'
            else:
                result_text = 'nope'
                
url = f"https://api.sportsdata.io/v3/mlb/scores/json/Games/2025"
api_key = "86f6d790e07d4c4cacddef80790bec22"  # Keep API keys private!
headers = {"Ocp-Apim-Subscription-Key": api_key}  # Some APIs require headers

response = requests.get(url, headers=headers)
schedules = response.json()

lads = []

for schedule in schedules:
    if schedule['AwayTeam'] == 'LAD' or schedule['HomeTeam'] == 'LAD':
        lads.append(schedule)
        
delta = timedelta(days=1000)

for lad in lads:
    game_date = datetime.strptime(lad['DateTime'], "%Y-%m-%dT%H:%M:%S")
    btwn = game_date - est_time.replace(tzinfo=None)
    if btwn < delta and btwn >= timedelta(days=0):
        delta = btwn
        home_team = lad['HomeTeam']
        away_team = lad['AwayTeam']
        gamer = game_date.date().strftime('%Y-%m-%d')
        

# Generate HTML content
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>did the dodgers win</title>
    <style>
        body {{
            background-color: #005A9C; /* Dodger Blue */
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            align-items: center;
            flex-direction: column;
            height: 100vh;
            margin: 0;
            text-align: center;
        }}

        .container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            margin-top: 20px; /* Ensure some top spacing */
        }}

        h1 {{
            font-size: 3em;
            margin-bottom: 0.5em; /* Add some spacing below the header */
        }}

        p {{
            font-size: 1.5em;
            margin: 0.5em 0;
        }}

        img {{
            width: 80%; /* Makes the image take 80% of the container width */
            max-width: 600px; /* Ensure the image doesn't get too large */
            height: auto; /* Maintain aspect ratio */
            margin-top: 20px; /* Add spacing between text and image */
        }}

        .spacer {{
            margin: 2em 0; /* Adds vertical spacing */
        }}

        .small-text {{
            font-size: 0.8em; /* Smaller font size */
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>did the dodgers win?</h1>
        <p>{result_text}</p>
        <p>up next: {gamer}, {away_team} @ {home_team}</p>
        <div class="spacer"></div>
        <div class="spacer"></div>
        <div class="spacer"></div>
        <p class="small-text">last updated: {est}</p>
    </div>
</body>
</html>
'''

# Write the HTML to a file
with open("index.html", "w") as file:
    file.write(html_content)
