from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# Table with season 21-22 stats
url = 'https://spbhl.ru/StatsPlayer?SeasonID=17'

driver = webdriver.Chrome()
driver.get(url)

# Variables that will be stored for each player
csv_cols = ["Name", "Player's Link", "Player's Number", "Team Name", "Team Link", "Role",
            "Number of Games", "Points", "Goals", "Assists", "Penalty Time"]
csv_rows = []
temp_row = []

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.find('table', id="StatsGridView")

    for row in rows.contents[1]:
        if hasattr(row, 'contents'):  # check if not an empty row
            phl = row.find('a', id='PlayerHyperLink')
            if phl is not None:
                if phl.text is not None:  # check if not a header of table (actual data row)
                    print('\n')
                    # Add name of the player
                    temp_row.append(phl.text)
                    # Add player link
                    temp_row.append(phl['href'])

                    # Find and add player number w/o '№'
                    p_n = row.find('span', class_='secondary label round')
                    # If player has a number
                    if p_n is not None:
                        temp_row.append(p_n.text.strip('№'))
                    else:
                        temp_row.append(None)

                    # Find and add team name and link
                    thl = row.find('a', id='TeamHyperLink')
                    temp_row.append(thl.text)
                    temp_row.append(thl['href'])

                    # Find and add stats
                    try:
                        temp_row.append(row.select_one("tr td:nth-of-type(5)").text)
                    except AttributeError:
                        temp_row.append(None)

                    try:
                        temp_row.append(row.select_one("tr td:nth-of-type(6)").text)
                    except AttributeError:
                        temp_row.append(None)

                    try:
                        temp_row.append(row.select_one("tr td:nth-of-type(7)").text)
                    except AttributeError:
                        temp_row.append(None)

                    try:
                        temp_row.append(row.select_one("tr td:nth-of-type(9)").text)
                    except AttributeError:
                        temp_row.append(None)

                    try:
                        temp_row.append(row.select_one("tr td:nth-of-type(10)").text)
                    except AttributeError:
                        temp_row.append(None)

                    try:
                        temp_row.append(row.select_one("tr td:nth-of-type(12)").text)
                    except AttributeError:
                        temp_row.append(None)

                    csv_rows.append(temp_row)
                    temp_row = []

    # Click to the rest of the pages
    cur_pages = soup.find('span', class_='current-page')
    el = cur_pages.parent.next_sibling
    if el == '\n':  # If last page, then stop
        break
    for e in el:
        href_to_click = e.get('href')

    element = driver.find_element(By.XPATH, '//a[@href="' + href_to_click + '"]')
    element.click()

with open('data_21_22.csv', 'w') as f:
    write = csv.writer(f)

    write.writerow(csv_cols)
    write.writerows(csv_rows)
