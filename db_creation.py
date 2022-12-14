import psycopg2
from getpass import getpass

user_password = getpass(prompt="Enter password: ")

with psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password=user_password) as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams(
            team_name VARCHAR ( 50 ) UNIQUE NOT NULL,
            team_link VARCHAR ( 255 ) UNIQUE NOT NULL PRIMARY KEY           
        );
        CREATE TABLE IF NOT EXISTS players(
            name VARCHAR ( 50 ) NOT NULL,
            player_link VARCHAR ( 255 ) UNIQUE NOT NULL PRIMARY KEY,
            role VARCHAR ( 8 ),
            player_number INT,
            team_link VARCHAR ( 255 ),
            FOREIGN KEY (team_link)
                REFERENCES teams (team_link)
        );
        CREATE TABLE IF NOT EXISTS tournaments(
            t_id SERIAL PRIMARY KEY,
            t_name varchar ( 50 ) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stats(
            player_link VARCHAR ( 255 ) NOT NULL,
            t_id INT NOT NULL,
            PRIMARY KEY (player_link, t_id),
            FOREIGN KEY (player_link)
                REFERENCES players (player_link),
            FOREIGN KEY (t_id)
                REFERENCES tournaments (t_id),
            n_games INT NOT NULL,
            pts INT NOT NULL,
            goals INT NOT NULL,
            assists INT NOT NULL,
            penalty_time INT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS user(
            user_id SERIAL PRIMARY KEY,
            user_points INT NOT NULL DEFAULT 0,
            user_dust INT NOT NULL DEFAULT 0
        );
    """)        # TODO: how to implement deck_id? Hash?

