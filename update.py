import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

# Fetch the web page
url = 'https://www.baseball-reference.com/teams/LAD/2024-schedule-scores.shtml'
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

results = []
upcoming = []

# Extract data
span_tags = soup.find_all('span', class_='poptip')
for span in span_tags:
    tip_text = span.get('tip')
    if tip_text:
        if 'lost' in tip_text or 'beat' in tip_text:
            results.append(tip_text)
        elif 'Off Day' not in tip_text and 'All-Star Game' not in tip_text:
            upcoming.append(tip_text)

# Determine if the Dodgers won
if 'lost' in results[-1]:
    result_text = 'nope'
elif 'beat' in results[-1]:
    result_text = 'yep'
else:
    result_text = "no clue"

# Get the upcoming game info
upcoming_game = upcoming[0] if upcoming else "No upcoming games"

# Get the current date and time in UTC
utc_now = datetime.utcnow()

# Convert UTC time to EST/EDT
utc_zone = pytz.utc
est_zone = pytz.timezone('America/New_York')

utc_now = utc_zone.localize(utc_now)
est_time = utc_now.astimezone(est_zone)

# Format date and time
formatted_date_time = est_time.strftime('%Y-%m-%d %H:%M:%S %Z')

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
            flex-direction: column;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            text-align: center;
        }}

        .container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}

        h1 {{
            font-size: 3em;
        }}

        p {{
            font-size: 1.5em;
            margin: 0.5em 0;
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
        <p>up next: {upcoming_game}</p>
        <div class="spacer"></div>
        <div class="spacer"></div>
        <div class="spacer"></div>
        <p class="small-text">last updated: {formatted_date_time}</p>
    </div>
</body>
</html>
'''

# Write the HTML to a file
with open("index.html", "w") as file:
    file.write(html_content)
