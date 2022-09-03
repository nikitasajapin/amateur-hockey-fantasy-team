from bs4 import BeautifulSoup
import requests


# Table with season 21-22 stats
url = 'https://spbhl.ru/StatsPlayer?SeasonID=17'

page = requests.get(url)
print(page.status_code)

# Variables that will be stored for each player
name = []
player_number = []
player_link = []
team_name = []
team_link = []
role = []
n_games = []
pts = []
pts_mean = []
goals = []
assists = []
penalty_time = []
penalty_mean_time = []

soup = BeautifulSoup(page.text, "html.parser")
rows = soup.find('table', id="StatsGridView")

for row in rows:
    if hasattr(row, 'contents'):            # check if not an empty row
        phl = row.find('a', id='PlayerHyperLink')
        if phl is not None:
            if phl.text is not None:        # check if not a header of table (actual data row)
                print('\n')
                name.append(phl.text)               # Add name of the player
                player_link.append(phl['href'])     # Add player link

                # Find and add player number w/o '№'
                p_n = row.find('span', class_='secondary label round')
                # If player has a number
                if p_n is not None:
                    player_number.append(p_n.text.strip('№'))
                else:
                    player_number.append(None)

                # Find and add team name and link
                thl = row.find('a', id='TeamHyperLink')
                team_name.append(thl.text)
                team_link.append(thl['href'])

                # Find and add stats
                try:
                    role.append(row.select_one("tr td:nth-of-type(5)").text)
                except AttributeError:
                    role.append(None)

                try:
                    n_games.append(row.select_one("tr td:nth-of-type(6)").text)
                except AttributeError:
                    n_games.append(None)

                try:
                    pts.append(row.select_one("tr td:nth-of-type(7)").text)
                except AttributeError:
                    pts.append(None)

                try:
                    pts_mean.append(row.select_one("tr td:nth-of-type(8)").text)
                except AttributeError:
                    pts_mean.append(None)

                try:
                    goals.append(row.select_one("tr td:nth-of-type(9)").text)
                except AttributeError:
                    goals.append(None)

                try:
                    assists.append(row.select_one("tr td:nth-of-type(10)").text)
                except AttributeError:
                    assists.append(None)

                try:
                    penalty_time.append(row.select_one("tr td:nth-of-type(12)").text)
                except AttributeError:
                    penalty_time.append(None)

                try:
                    penalty_mean_time.append(row.select_one("tr td:nth-of-type(13)").text)
                except AttributeError:
                    penalty_mean_time.append(None)

                print(thl.text)
                print(player_number[-1])
                print(phl.text)
