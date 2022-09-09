import psycopg2
from getpass import getpass
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By


spbhl_t_id = 5786           # ЗаряД Cup (Старт А)
url = f'https://spbhl.ru/Players?SeasonID=18&TournamentID={spbhl_t_id}'

driver = webdriver.Chrome()
driver.get(url)

user_password = getpass(prompt="Enter password: ")
temp_row = []
while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.find('table', style="border-collapse:collapse;")

    for row in rows.contents[1]:
        if hasattr(row, 'contents'):  # check if not an empty row
            phl = row.find('a', id='PlayerHyperLink')
            if phl is not None:
                if phl.text is not None:  # check if not a header of table (actual data row)

                    # print('\n')
                    # Add name of the player
                    p_name = phl.text
                    # print(p_name)
                    # Add player link
                    p_link = phl['href']

                    # Find and add player number w/o '№'
                    p_n = row.find('span', class_='label')
                    # If player has a number
                    if p_n is not None:
                        p_number = p_n.text.strip('№')
                    else:
                        p_number = '0'

                    # Find and add team name and link
                    thl = row.find('a', id='TeamHyperLink')
                    t_name = thl.text
                    t_link = thl['href']

                    # Find and add stats

                    try:
                        p_role = row.select_one("tr td:nth-of-type(6)").text
                    except AttributeError:
                        p_role = 'N/A'

                    with psycopg2.connect(
                            host="localhost",
                            database="postgres",
                            user="postgres",
                            password=user_password) as conn:
                        cur = conn.cursor()
                        cur.execute(f"""
                            INSERT INTO teams
                                (team_name, team_link)
                            VALUES
                                ('{t_name}', '{t_link}')
                            ON CONFLICT DO NOTHING;
                        """)

                        cur.execute(f"""
                            SELECT team_id
                            FROM teams
                            WHERE team_name = '{t_name}'
                        """)
                        team_id = cur.fetchone()[0]

                        cur.execute(f"""
                            INSERT INTO players
                                (name, player_link, role, player_number, team_id)
                            VALUES
                                ('{p_name}', '{p_link}', '{p_role}', {p_number}, {team_id})
                            ON CONFLICT DO NOTHING;
                        """)

    # Click to the rest of the pages
    cur_pages = soup.find('span', class_='current-page')
    el = cur_pages.parent.next_sibling
    if el == '\n':  # If last page, then stop
        break
    for e in el:
        href_to_click = e.get('href')

    element = driver.find_element(By.XPATH, '//a[@href="' + href_to_click + '"]')
    element.click()