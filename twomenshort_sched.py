import requests
import re
import json
from datetime import datetime
import pytz
from time import sleep

def twomenshort_sched():
    ashl_url = "https://www.ashl.ca/stats-and-schedules/ashl/york-summer/"
    sports_ninja = "https://canlanstats.sportninja.com/org/"
    js_url = "https://canlanstats.sportninja.com/static/js/"
    auth_url = "https://canlan2-api.sportninja.net/auth/refresh"
    games_url = "https://canlan2-api.sportninja.net/schedules/Xgg6wG5K20gnzLKS/games?order=asc&exclude_cancelled_games=1&team_id=IfFl4yJ3V4rlum6a"

    def get_max_team_len(max_team_len):
        for game in games["data"]:
            team_full = game["homeTeam"]["name"] + " Vs. " + game["visitingTeam"]["name"]
            if len(team_full) > max_team_len:
                max_team_len = len(team_full)
        return max_team_len

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    }

    req = requests.get(ashl_url, headers=headers)
    weird_string = re.search('(?<=renderOrg\(")\w*', req.text)[0]
    req = requests.get(sports_ninja + weird_string)
    js_name = re.search('(?<=js\/main\.)\w*', req.text)[0]
    req = requests.get(js_url + "main." + js_name + ".js")
    auth = re.findall('v2\.local\.[^"]*', req.text)

    headers = {
            "Authorization" : auth[0]
    }

    req = requests.post(auth_url, headers=headers)
    auth_obj = json.loads(req.text)

#print(auth_obj["access_token"])

    headers = {
            "Authorization" : auth_obj["access_token"]
    }

    req = requests.get(games_url, headers=headers)
    games = json.loads(req.text)

    start_time = games["data"][0]["starts_at"]

    max_team_len = 0
    max_length = get_max_team_len(max_team_len)

    output = ''
    for game in games["data"]:
        start_time = game["starts_at"]
        rink = game["facility"]["name"]
        dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z")
        eastern = pytz.timezone('US/Eastern')
        dt = dt.astimezone(eastern)
        print(dt.strftime("%m-%d %I:%M %p"), end=" | ")
        output += dt.strftime("%m-%d %I:%M %p") + " | "
        team_full = game["homeTeam"]["name"] + " Vs. " + game["visitingTeam"]["name"]
        print("{text:{width}}".format(text=team_full, width=max_length), end = " | ")
        output += "{text:{width}}".format(text=team_full, width=max_length) + " | "
        #print(f"{home_team} Vs. {visiting_team}", end=" | ")
        print(rink)
        output += rink + "\n"
    return output
