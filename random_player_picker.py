import psycopg2
from getpass import getpass
import random

user_password = getpass(prompt="Enter password: ")

with psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password='user_password') as conn:
    cur = conn.cursor()     # TODO: retrieve player link, not name
    cur.execute("""
        SELECT name
        FROM players;  
    """)
    player_names = cur.fetchall()
    cards = 50
    user_deck = []
    for i in range(0, 50):  # TODO: add minimum of x good cards
        user_deck.append(player_names[random.randint(0, len(player_names))])
    print(user_deck)
    # Some code here
