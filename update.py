import requests
from datetime import datetime, timedelta
import pytz
import pandas as pd

teams = {
      'arizona diamondbacks': {
          'abbr': 'ARI'
        , 'color': '#E3D4AD' ## gold
        , 'nickname': 'diamondbacks'}
    , 'atlanta braves': {
          'abbr': 'ATL'
        , 'color': '#CE1141' ## red
        , 'nickname': 'braves'}
    , 'baltimore orioles': {
          'abbr': 'BAL'
        , 'color': '#DF4601' ## orange
        , 'nickname': 'orioles'}
    , 'boston red sox': {
          'abbr': 'BOS'
        , 'color': '#BD3039' ## red
        , 'nickname': 'red sox'}
    , 'chicago cubs': {
          'abbr': 'CHC'
        , 'color': '#0E3386' ## blue
        , 'nickname': 'cubs'}
    , 'chicago white sox': {
          'abbr': 'CHW'
        , 'color': '#C4CED4' ## silver
        , 'nickname': 'white sox'}
    , 'cincinnati reds': {
          'abbr': 'CIN'
        , 'color': '#C6011F' ## red
        , 'nickname': 'reds'}
    , 'cleveland guardians': {
          'abbr': 'CLE'
        , 'color': '#E50022' ## red
        , 'nickname': 'guardians'}
    , 'colorado rockies': {
          'abbr': 'COL'
        , 'color': '#333366' ## purple
        , 'nickname': 'rockies'}
    , 'detroit tigers': {
          'abbr': 'DET'
        , 'color': '#FA4616' ## orange
        , 'nickname': 'tigers'}
    , 'homeless athletics': {
          'abbr': 'ATH'
        , 'color': '#003831' ## green
        , 'nickname': 'athletics'}
    , 'houston astros': {
          'abbr': 'HOU'
        , 'color': '#EB6E1F' ## orange
        , 'nickname': 'astros'}
    , 'kansas city royals': {
          'abbr': 'KC'
        , 'color': '#004687' ## blue
        , 'nickname': 'royals'}
    , 'los angeles angels': {
          'abbr': 'LAA'
        , 'color': '#BA0021' ## red
        , 'nickname': 'angels'}
    , 'los angeles dodgers': {
          'abbr': 'LAD'
        , 'color': '#005A9C' ## blue
        , 'nickname': 'dodgers'}
    , 'miami marlins': {
          'abbr': 'MIA'
        , 'color': '#00A3E0' ## blue
        , 'nickname': 'marlins'}
    , 'milwaukee brewers': {
          'abbr': 'MIL'
        , 'color': '#FFC52F' ## yellow
        , 'nickname': 'brewers'}
    , 'minnesota twins': {
          'abbr': 'MIN'
        , 'color': '#D31145' ## red
        , 'nickname': 'twins'}
    , 'new york mets': {
          'abbr': 'NYM'
        , 'color': '#FF5910' ## orange
        , 'nickname': 'mets'}
    , 'new york yankees': {
          'abbr': 'NYY'
        , 'color': '#C4CED3' ## gray
        , 'nickname': 'yankees'}
    , 'philadelphia phillies': {
          'abbr': 'PHI'
        , 'color': '#E81828' ## red
        , 'nickname': 'phillies'}
    , 'pittsburgh pirates': {
          'abbr': 'PIT'
        , 'color': '#FDB827' ## gold
        , 'nickname': 'pirates'}
    , 'san diego padres': {
          'abbr': 'SD'
        , 'color': '#FFC425' ## gold
        , 'nickname': 'padres'}
    , 'san francisco giants': {
          'abbr': 'SF'
        , 'color': '#FD5A1E' ## orange
        , 'nickname': 'giants'}
    , 'seattle mariners': {
          'abbr': 'SEA'
        , 'color': '#005C5C' ## green
        , 'nickname': 'mariners'}
    , 'st. louis cardinals': {
          'abbr': 'STL'
        , 'color': '#C41E3A' ## red
        , 'nickname': 'cardinals'}
    , 'tampa bay rays': {
          'abbr': 'TB'
        , 'color': '#8FBCE6' ## blue
        , 'nickname': 'rays'}
    , 'texas rangers': {
          'abbr': 'TEX'
        , 'color': '#003278' ## blue
        , 'nickname': 'rangers'}
    , 'toronto blue jays': {
          'abbr': 'TOR'
        , 'color': '#134A8E' ## blue
        , 'nickname': 'blue jays'}
    , 'washington nationals': {
          'abbr': 'WSH'
        , 'color': '#AB0003' ## red
        , 'nickname': 'nationals'}
}

utc_now = datetime.utcnow()
utc_zone = pytz.utc
est_zone = pytz.timezone('America/New_York')
utc_now = utc_zone.localize(utc_now)
est_time = utc_now.astimezone(est_zone)
date = (est_time - timedelta(days=1)).strftime('%Y-%m-%d')
est = est_time.strftime('%Y-%m-%d %H:%M:%S %Z')

url = f'https://api.sportsdata.io/v3/mlb/scores/json/ScoresBasic/{date}'
api_key = "86f6d790e07d4c4cacddef80790bec22"

headers = {"Ocp-Apim-Subscription-Key": api_key}

response = requests.get(url, headers=headers)

games = response.json()
games = pd.DataFrame(games)
games = games.sort_values(by='GameEndDateTime', ascending=False).reset_index(drop=True)

def outcome(interest, games):

    games = games[(games['HomeTeam'] == interest) | (games['AwayTeam'] == interest)]

    if len(games) == 0:
        result = 'no game yesterday'
        return result

    games = games.iloc[0]

    team = 'AwayTeamRuns'
    vs = 'HomeTeamRuns'
    result = 'nope'

    if games['Status'] != 'Final':
        result = 'up in the air'
    if games['HomeTeam'] == interest:
        team = 'HomeTeamRuns'
        vs = 'AwayTeamRuns'

    if games[team] > games[vs]:
        result = 'yep'

    if interest == 'COL': ## did the rockies lose?
        result = {'yep': 'nope', 'nope': 'yep'}.get(result, result)

    return result

url = f'https://api.sportsdata.io/v3/mlb/scores/json/Games/2025'
api_key = "86f6d790e07d4c4cacddef80790bec22"  # Keep API keys private!
headers = {"Ocp-Apim-Subscription-Key": api_key}  # Some APIs require headers
response = requests.get(url, headers=headers)
schedules = response.json()

schedules = pd.DataFrame(schedules)
final = schedules[schedules['Status'] == 'Final']
completed = schedules[schedules['Status'] == 'Completed']
schedules = schedules[schedules['Status'] == 'Scheduled']
schedules = schedules.sort_values(by='Day').reset_index(drop=True)

def upcoming(interest, schedules):

    schedule = schedules[(schedules['HomeTeam'] == interest) | (schedules['AwayTeam'] == interest)].reset_index(drop=True)

    if len(schedule) == 0:
        up_next = 'offseason'
        return up_next

    schedule = schedule.iloc[0]
    game_date = datetime.strptime(schedule['Day'], "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')
    up_next = f"{game_date}, {schedule['AwayTeam']} @ {schedule['HomeTeam']}"
    return up_next

def record(interest, final):

    final = final[(final['HomeTeam'] == interest) | (final['AwayTeam'] == interest)].reset_index(drop=True)
    final.loc[(final['HomeTeam'] == interest) & (final['HomeTeamRuns'] > final['AwayTeamRuns']), 'wins'] = 1
    final.loc[(final['AwayTeam'] == interest) & (final['HomeTeamRuns'] < final['AwayTeamRuns']), 'wins'] = 1
    final.loc[(final['HomeTeam'] == interest) & (final['HomeTeamRuns'] < final['AwayTeamRuns']), 'losses'] = 1
    final.loc[(final['AwayTeam'] == interest) & (final['HomeTeamRuns'] > final['AwayTeamRuns']), 'losses'] = 1
    final.loc[final['HomeTeamRuns'] == final['AwayTeamRuns'], 'ties'] = 1

    wins = str(int(final.wins.sum()))
    losses = str(int(final.losses.sum()))
    ties = str(int(final.ties.sum()))
    record = wins + '-' + losses + '-' + ties
    
    return record

def web(result, record, up_next, est, title, color):  

    page = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>did the dodgers win</title>
            <style>
                body {{
                    background-color: {color}; /* Team Color */
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
                <h1>{title}</h1>
                <p>{result}</p>
                <p>record: {record}</p>
                <p>up next: {up_next}</p>
                <div class="spacer"></div>
                <div class="spacer"></div>
                <div class="spacer"></div>
                <p class="small-text">last updated: {est}</p>
                <div class="spacer"></div>
                <button onclick="window.location.href='index.html'" style="padding:
                    10px 20px; font-size: 1em; cursor: pointer;">
                    go back
                </button>
            </div>
        </body>
        </html>
        '''

    return page
 

for team, info in teams.items():

    abbr = info['abbr']
    color = info['color']
    nickname = info['nickname']

    if abbr == 'COL':
        title = f'did the {nickname} lose'
    else:
        title = f'did the {nickname} win'

    result = outcome(abbr, games)
    season = record(abbr, final)
    up_next = upcoming(abbr, schedules)
    page = web(result, season, up_next, est, title, color)

    with open(f"{nickname}.html", "w") as file:
        file.write(page)


index = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>baseball</title>
        <style>
            * { box-sizing: border-box; }

            body {
                margin: 0;
                height: 100vh;
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 20px;
                padding: 20px;
                background: #f5f5f5;
            }

            h1 {
                margin: 0;
                font-size: clamp(1.5rem, 5vw, 2.5rem);
                color: #333;
            }

            .controls {
                display: flex;
                gap: 15px;
                align-items: center;
                flex-wrap: wrap;
            }

            select, button {
                padding: 12px 16px;
                font-size: 16px;
                border: 2px solid #ddd;
                border-radius: 8px;
                background: white;
            }

            select {
                min-width: 200px;
            }

            button {
                background: #2c5234;
                color: white;
                border-color: #2c5234;
                cursor: pointer;
                font-weight: 600;
            }

            button:hover {
                background: #1a3020;
            }

            button:disabled {
                background: #ccc;
                cursor: not-allowed;
            }

            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                right: 0;
                padding: 15px;
                text-align: center;
                font-size: 0.9em;
                color: #666;
                background: white;
                border-top: 1px solid #eee;
            }

            @media (max-width: 600px) {
                .controls {
                    flex-direction: column;
                    width: 100%;
                }

                select, button {
                    width: 100%;
                    max-width: 300px;
                }

                .footer {
                    position: relative;
                    margin-top: 40px;
                }
            }
        </style>
    </head>
    <body>
        <div class="controls">
            <h1>pick your team</h1>
            <select id="teamDropdown">
                <option value="">select a team...</option>
                <option value="diamondbacks">arizona diamondbacks</option>
                <option value="braves">atlanta braves</option>
                <option value="orioles">baltimore orioles</option>
                <option value="red sox">boston red sox</option>
                <option value="cubs">chicago cubs</option>
                <option value="white sox">chicago white sox</option>
                <option value="reds">cincinnati reds</option>
                <option value="guardians">cleveland guardians</option>
                <option value="rockies">colorado rockies</option>
                <option value="tigers">detroit tigers</option>
                <option value="athletics">homeless athletics</option>
                <option value="astros">houston astros</option>
                <option value="royals">kansas city royals</option>
                <option value="angels">los angeles angels</option>
                <option value="dodgers">los angeles dodgers</option>
                <option value="marlins">miami marlins</option>
                <option value="brewers">milwaukee brewers</option>
                <option value="twins">minnesota twins</option>
                <option value="mets">new york mets</option>
                <option value="yankees">new york yankees</option>
                <option value="phillies">philadelphia phillies</option>
                <option value="pirates">pittsburgh pirates</option>
                <option value="padres">san diego padres</option>
                <option value="giants">san francisco giants</option>
                <option value="mariners">seattle mariners</option>
                <option value="cardinals">st. louis cardinals</option>
                <option value="rays">tampa bay rays</option>
                <option value="rangers">texas rangers</option>
                <option value="blue jays">toronto blue jays</option>
                <option value="nationals">washington nationals</option>
            </select>
            <button onclick="goToTeam()" id="btn">select</button>
        </div>

        <div class="footer">
            This website pulls data from sportsdata.io's free API. Results may not be accurate.
            Extension of "Did The Dodgers Win".
        </div>

        <script>
            const dropdown = document.getElementById('teamDropdown');
            const btn = document.getElementById('btn');

            dropdown.onchange = () => btn.disabled = !dropdown.value;
            btn.disabled = true;

            function goToTeam() {
                const team = dropdown.value;
                if (team) {
                    window.location.href = `${team}.html`;
                }
            }
        </script>
    </body>
    </html>
    '''

with open("index.html", "w") as file:
    file.write(index)
