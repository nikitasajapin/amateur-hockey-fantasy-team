from bs4 import BeautifulSoup
import requests


url = 'https://spbhl.ru/StatsPlayer?SeasonID=17'

page = requests.get(url)
print(page.status_code)

name = []
role = []
games = []
pts = []
pts_mean = []
goals = []
assists = []
bench_time = []

soup = BeautifulSoup(page.text, "html.parser")
t_name = soup.findAll('a', href=True, id='PlayerHyperLink')
#print(soup)
for data in t_name:
    if data.text is not None:
        name.append(data.text)
print(name)