#http://nbasense.com/nba-api/ - documentation

import urllib.request

class Match:
    teams = ""
    date = ""
    time = ""

    def __init__(self, teams, date, time):
        self.teams = teams
        self.date = date
        self.time = time

    def print(self):
        print(self.teams, "|", self.date, "|", self.time)


def convertTime(time, month):
    result = "HH:MM"
    hour = int(time[:2])
    min = time[3:]

    #winter
    if (month >= 11) or (month <= 3):
        hour += 1
    #summer
    else:
        hour += 2
        
    if hour >= 24:
        hour = hour - 24

    return result.replace("MM", min).replace("HH", str(hour))

matches = []
date = ""
time = "" 
teams = ""

while True:
    season = input("Season to get: ");
    if not season : season = "2019"
    requestUrl = "http://data.nba.com/data/10s/v2015/json/mobile_teams/nba/TOREPLACE/league/00_full_schedule.json"
    requestUrl = requestUrl.replace("TOREPLACE", season)

    try:
        with urllib.request.urlopen(requestUrl) as response:
            print("Loading", season + "...")
            line = str(response.readline(), 'utf-8')
            while line:
                if "gcode" in line:
                    words = line.split()
                    word = words[1].strip()
                    teams = words[1][10:len(word)-2]
                elif "gdtutc" in line:
                    line = line.strip()
                    date = line[11:len(line)-2]
                elif "utctm" in line:
                    line = line.strip()
                    time = line[10:len(line)-2]
                    time = convertTime(time, int(date[5:7]))
                elif (teams != "") and (date != "") and (time != ""):
                    matches.append(Match(teams, date, time))
                    date = ""
                    time = "" 
                    teams = ""
                line = str(response.readline(), 'utf-8')
            print("DONE!")
            break

    except:
            print("Oops! Wrong season? Try again...")

while True:
    monthToShow = input("Month to display: ");
    if not monthToShow: break
    for match in matches:
        hour = int(match.time[:match.time.find(":")])
        if (hour >= 8) and (hour < 24) and (monthToShow == match.date[5:7]):
            match.print()
print("Finished!")