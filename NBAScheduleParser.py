#http://nbasense.com/nba-api/ - documentation

import urllib.request
import json
import datetime

START_HOUR = 7
END_HOUR = 24
FAVOURITE = {"DAL","LAL"}
WEEKDAYS = {"0": "Monday", "1": "Tuesday", "2": "Wednesday", "3": "Thursday", "4": "Friday", "5": "Saturday", "6": "Sunday"}

class Match:
    teams = ""
    dateTime = datetime.datetime(2000,1,1)

    def __init__(self, teams, dateTime):
        self.teams = teams
        self.dateTime = dateTime

    def print(self):
        comment = ""
        if any(favTeam in self.teams for favTeam in FAVOURITE):
            comment = "FAVOURITE!!!"
        print(self.teams, "|", self.dateTime, "|", '{:^9}'.format(WEEKDAYS[str(self.dateTime.weekday())]), "|", comment)

def convertDate(date):
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(date[11:13])
    minutes = int(date[14:16])
    return datetime.datetime(year, month, day, convertHour(hour, month), minutes)

def convertHour(hour, month):
    if (month >= 11) or (month <= 3): #winter time
        hour += 1
    else: #summer time
        hour += 2 
        
    if hour >= 24: #24H time format
        hour = hour - 24
    return hour

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
                dateTime = convertDate(startTimeUTC)
                matches.append(Match(teams, dateTime))
            print("DONE!")
            break
    except:
        print("Oops! Wrong season? Try again...")
#printing requested matches
while True:
    monthToShow = input("Month to display: ")
    if not monthToShow: break
    for match in matches:
        try:
            if (match.dateTime.hour >= START_HOUR) and (match.dateTime.hour < END_HOUR) and (int(monthToShow) == match.dateTime.month):
                match.print()
        except:
            print("Oops! Wrong month? Try again...")
            break
print("Finished!")