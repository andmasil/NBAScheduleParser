#http://nbasense.com/nba-api/ - documentation

import urllib.request
import json

START_HOUR = 7
END_HOUR = 24
FAVOURITE = {"DAL","LAL"}

class Match:
    teams = ""
    date = ""
    time = ""

    def __init__(self, teams, date, time):
        self.teams = teams
        self.date = date
        self.time = time

    def print(self):
        comment = ""
        if any(favTeam in self.teams for favTeam in FAVOURITE):
            comment = "FAVOURITE"
        print(self.teams, "|", self.date, "|", self.time, comment)

def convertTime(time, month):
    result = "HH:MM"
    hour = int(time[:2])
    min = time[3:]

    if (month >= 11) or (month <= 3): #winter time
        hour += 1
    else: #summer time
        hour += 2 
        
    if hour >= 24: #24H time format
        hour = hour - 24

    return result.replace("MM", min).replace("HH", str(hour))

#geting seazon schedule
matches = []
while True:
    season = input("Season to get: ");
    if not season : season = "2019"
    requestUrl = "http://data.nba.net/prod/v2/{year}/schedule.json".replace("{year}", season)

    try:
        with urllib.request.urlopen(requestUrl) as url:
            print("Loading", season + "...")
            data = json.loads(url.read().decode())
            data = data["league"]["standard"]

            for match in data:
                gameUrlCode = match["gameUrlCode"]
                startTimeUTC = match["startTimeUTC"]
                teams = gameUrlCode[9:]
                date = startTimeUTC[:10]
                time = convertTime(startTimeUTC[11:16], int(date[5:7]))
                matches.append(Match(teams, date, time))
            print("DONE!")
            break
    except:
            print("Oops! Wrong season? Try again...")
#printing requested matches
while True:
    monthToShow = input("Month to display: ")
    if len(monthToShow) is 1 : monthToShow = "0" + monthToShow
    if not monthToShow: break
    for match in matches:
        hour = int(match.time[:match.time.find(":")])
        if (hour >= START_HOUR) and (hour < END_HOUR) and (monthToShow == match.date[5:7]):
            match.print()
print("Finished!")