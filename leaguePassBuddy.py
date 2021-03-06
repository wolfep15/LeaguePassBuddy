import nba_py
import datetime
from nba_py import team


# Takes 2 team IDs
# returns the difference in net rating between those 2 teams
def calcComp(homeID, awayID):
    # Calculate home and away net ratings
    away = nba_py.team.TeamSummary(team_id=awayID, season='2017-18').season_ranks()
    awayNetRtg = away[0]['PTS_PG'] - away[0]['OPP_PTS_PG']
    home = nba_py.team.TeamSummary(team_id=homeID, season='2017-18').season_ranks()
    homeNetRtg = home[0]['PTS_PG'] - home[0]['OPP_PTS_PG']

    # Calculate difference between netrtgs
    competitiveness = abs(homeNetRtg - awayNetRtg)
    return competitiveness

# Takes a game json object and the home and away ID of
# the 2 teams in that game
# Prints the information the specified game
def printGame(game, homeID, awayID):
    homeDetails = nba_py.team.TeamDetails(team_id=homeID).background()[0]
    awayDetails = nba_py.team.TeamDetails(team_id=awayID).background()[0]
    homeTeam = homeDetails["CITY"] + " " + homeDetails["NICKNAME"]
    awayTeam = awayDetails["CITY"] + " " + awayDetails["NICKNAME"]

    info = "The most interesting game tonight is " + awayTeam + " at " + homeTeam
    print(info)
    status = game["GAME_STATUS_TEXT"]

    # check if game has already started
    if "Qtr" not in status:
        print("It starts at " + status)
    else:
        print("It's on now!")

# Prints out most competitive game based on net rtg differential
def main():
    # get date and that date's game
    today = datetime.datetime.now()
    todaysData = nba_py.Scoreboard(month=today.month, day=today.day, year=today.year)
    todaysGames = todaysData.game_header()

    mostInteresting = {}
    homeID = 0
    awayID = 0
    foundOne = 0
    currComp = 99999

    # Iterate through all of today's games
    for game in todaysGames:

        # Get info for current game
        currAwayId = game["VISITOR_TEAM_ID"]
        currHomeId = game["HOME_TEAM_ID"]
        currStatus = game["GAME_STATUS_TEXT"]

        competitiveness = calcComp(currHomeId, currAwayId)

        if competitiveness < currComp and currStatus != 'Final':
            currComp = competitiveness
            mostInteresting = game
            homeID = currHomeId
            awayID = currAwayId
            foundOne = 1

    # If a game has been found, print info about it
    if foundOne == 1:
        printGame(mostInteresting, homeID, awayID)

    # Otherwise just return no items found message
    else:
        print("No games left today. Sorry!")


if __name__ == "__main__": main()
