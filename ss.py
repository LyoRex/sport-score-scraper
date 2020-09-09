import sys

from urllib.request import urlopen as urlreq
from bs4 import BeautifulSoup as soup
from bs4 import Comment
from datetime import date, datetime, timedelta
from urllib.error import HTTPError

# Command line input: python score_scrape.py <sys.argv[1]> <sys.argv[2]> <sys.argv[3]> <sys.argv[4]>

def nfl_get_num_weeks(year):
    maxWeek = 1

    url = 'https://www.pro-football-reference.com/years/' + year + '/week_1.htm'

    try:
        # open connection and get page html
        urlClient = urlreq(url)
        page_html = urlClient.read()
        urlClient.close()
    except:
        print("Could not open page: " + url)

    page_soup = soup(page_html, "html.parser")

    maxWeek = int(str(page_soup.find("div", {"class":"section_wrapper"}).find(string=lambda text: isinstance(text, Comment))).count("/week_"))

    return maxWeek
def nfl_scores():
    # initialize year to current year and week to first week
    year = str(date.today().year)
    week = "1"
    maxWeek = 1
    try:
        if len(sys.argv) == 4:
            if len(str(sys.argv[2])) == 4:
                year = str(sys.argv[2])
            else:
                print("Must input a valid year!")
                raise Exception
            maxWeek = nfl_get_num_weeks(str(year))
            if int(sys.argv[3]) > 0:
                if int(sys.argv[3]) <= maxWeek:
                    week = str(sys.argv[3])
                else:
                    print("NFL " + year + " only has " + str(maxWeek) + " weeks!")
                    raise Exception
            else:
                print("Must enter a positive value for week!")
                raise Exception
        else:
            print("Arguments for football are <year> <week>")
            raise Exception
    except:
        print("One or more of your arguments are not valid!")

    #Pro Football Reference
    my_url = 'https://www.pro-football-reference.com/years/' + year + '/week_' + week + '.htm'

    pageExist = True
    try:
        # open connection and get page html
        urlClient = urlreq(my_url)
        page_html = urlClient.read()
        urlClient.close()
    except HTTPError:
        pageExist = False
        print("Page does not exist!")

    if pageExist:
        # initiate soup
        page_soup = soup(page_html, "html.parser")
        gamePosts = page_soup.findAll("div", {"class":"game_summary expanded nohover"})
        #header
        print("Getting scores from Week " + week + " of the " + year + " Season!")
        print("================================================")

        for post in gamePosts:
            gameDate = post.find("tr", {"class","date"}).text

            homeTeam = post.find("table", {"class","teams"}).tbody.select("tr")[1]
            homeTeamName = homeTeam.select("td")[0].text
            awayTeam = post.find("table", {"class","teams"}).tbody.select("tr")[2]
            awayTeamName = awayTeam.select("td")[0].text

            homeTeamPoints = homeTeam.select("td")[1].text
            awayTeamPoints = awayTeam.select("td")[1].text

            passYdName = post.find("table", {"class","stats"}).select("tr")[0].select("td")[1].text
            passYdPts = post.find("table", {"class","stats"}).select("tr")[0].select("td")[2].text

            rushYdName = post.find("table", {"class","stats"}).select("tr")[1].select("td")[1].text
            rushYdPts = post.find("table", {"class","stats"}).select("tr")[1].select("td")[2].text
            
            recYdName = post.find("table", {"class","stats"}).select("tr")[2].select("td")[1].text
            recYdPts = post.find("table", {"class","stats"}).select("tr")[2].select("td")[2].text

            winnerIndex = 1
            if post.find("table", {"class","teams"}).find("tbody").select("tr")[1] == post.find("tr",{"class","winner"}):
                winnerIndex = 1
            else:
                winnerIndex = 2
            
            print(gameDate + ":")
            print("(H) " + homeTeamName + " scored " + homeTeamPoints + " points.", end = " ")
            if winnerIndex == 1:
                print("[WINNER]")
            else:
                print()
            print("(A) " + awayTeamName + " scored " + awayTeamPoints + " points.", end = " ")
            if winnerIndex == 2:
                print("[WINNER]")
            else:
                print()
            
            print("\t-" + passYdName + " led in passing yards with " + passYdPts + " yards")
            print("\t-" + rushYdName + " led in rushing yards with " + rushYdPts + " yards")
            print("\t-" + recYdName + " led in receiving yards with " + recYdPts + " yards")
            
            print('------------------------------------------------------------')
            print()    
def nba_scores():
    # Set default date to current day
    month = str(date.today().month)
    day = str(date.today().day)
    year = str(date.today().year)
    # check for inputs
    try:
        if len(sys.argv) >= 3:   
            # input is today
            if sys.argv[2].lower() == "today" or sys.argv[2].lower() == "t":
                month = str(date.today().month) if len(str(date.today().month)) == 2 else "0" + str(date.today().month)
                day = str(date.today().day) if len(str(date.today().day)) == 2 else "0" + str(date.today().day)
                year = str(date.today().year)
            # input is yesterday
            elif sys.argv[2].lower() == "yesterday" or sys.argv[2].lower() == "y":
                daysBack = 1
                # set amount of days back
                if len(sys.argv) == 4:
                    if int(sys.argv[3]) >= 0:
                        daysBack = int(sys.argv[3])
                    else:
                        print("Can not go back negative days; going back 1 day instead!")

                # set month, day, and year
                newDate = date.today() - timedelta(daysBack)
                month = str(newDate.month)
                day = str(newDate.day)
                year = str(newDate.year)
            # date is given
            else:
                # input year is after current year
                if int(sys.argv[4]) > int(date.today().year):
                    validInDate = False
                elif int(sys.argv[4]) == int(date.today().year):
                    # input month is after current month
                    if int(sys.argv[2]) > int(date.today().month):
                        validInDate = False
                    elif int(sys.argv[2]) == int(date.today().month):
                        # input day is after current day
                        if int(sys.argv[3]) > int(date.today().day):
                            validInDate = False
                month = str(sys.argv[2])
                day = str(sys.argv[3])
                year = str(sys.argv[4])
    except:
        print("One or more of your arguments are not valid!")

    #Basketball Reference
    my_url = 'https://www.basketball-reference.com/boxscores/?month=' + month + '&day=' + day + '&year=' + year

    pageExist = True
    try:
        # open connection and get page html
        urlClient = urlreq(my_url)
        page_html = urlClient.read()
        urlClient.close()
    except HTTPError:
        pageExist = False
        print("Page does not exist!")
    
    if(pageExist):
        # html parsing
        page_soup = soup(page_html, "html.parser")
        # get all game posts
        gamePosts = page_soup.findAll("div", {"class":"game_summary expanded nohover"})

        # header
        print("Getting scores from " + month + "/" + day + "/" + year)
        print("=================================")

        # parse data for all games
        for post in gamePosts:
            leadScorer = post.find("table", {"class":"stats"}).tbody.tr.select('td')[1].text
            mostPoints = post.find("table", {"class":"stats"}).tbody.tr.select('td')[2].text
            
            homeTeam = post.select('table')[1].tbody.select('tr')[0].td.a.text
            awayTeam = post.select('table')[1].tbody.select('tr')[1].td.a.text

            winner = post.find("table", {"class":"teams"}).tbody.find("tr", {"class":"winner"})
            winnerTeam = winner.td.text
            winnerPoints = winner.find("td", {"class":"right"}).text
            
            loser = post.find("table", {"class":"teams"}).tbody.find("tr", {"class":"loser"})
            loserTeam = loser.td.text
            loserPoints = loser.find("td", {"class":"right"}).text

            print(("(H) " if homeTeam == winnerTeam else "(A) ") + winnerTeam + " scored " + winnerPoints + " points. [WINNER]")
            print(("(H) " if homeTeam == loserTeam else "(A) ") + loserTeam + " scored " + loserPoints + " points.")
            print("\t-The leading scorer was " + leadScorer + " with " + mostPoints + " points.")

            print('------------------------------------------------------------')
            print()
   


#############################
#                           #
#       START MAIN          #
#                           #
#############################
sport = "none"

try:
    sport = str(sys.argv[1])
    if(sys.argv[1] != "basketball" and sys.argv[1] != "b" and sys.argv[1] != "football" and sys.argv[1] != "f"):
        raise Exception
except:
    print("You must specify a sport ('basketball' or football')")

if(sport == "basketball" or sport == "b"):
    nba_scores()
elif(sport == "football" or sport == "f"):
    nfl_scores()
