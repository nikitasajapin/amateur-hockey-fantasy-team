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
            team_id SERIAL PRIMARY KEY UNIQUE,
            team_name VARCHAR ( 50 ) UNIQUE NOT NULL,
            team_link VARCHAR ( 255 ) UNIQUE NOT NULL           
        );
        CREATE TABLE IF NOT EXISTS players(
            player_id SERIAL PRIMARY KEY UNIQUE,
            name VARCHAR ( 50 ) NOT NULL,
            player_link VARCHAR ( 255 ) UNIQUE NOT NULL,
            role VARCHAR ( 8 ),
            player_number INT,
            team_id INT NOT NULL,
            FOREIGN KEY (team_id)
                REFERENCES teams (team_id)
        );
        CREATE TABLE IF NOT EXISTS tournaments(
            tr_id SERIAL PRIMARY KEY UNIQUE,
            tr_name varchar ( 50 ) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stats(
            player_id INT NOT NULL,
            tr_id INT NOT NULL,
            PRIMARY KEY (player_id, tr_id),
            FOREIGN KEY (player_id)
                REFERENCES players (player_id),
            FOREIGN KEY (tr_id)
                REFERENCES tournaments (tr_id),
            n_games INT NOT NULL,
            pts INT NOT NULL,
            goals INT NOT NULL,
            assists INT NOT NULL,
            penalty_time INT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS users(
            user_id SERIAL PRIMARY KEY UNIQUE,
            user_points INT NOT NULL DEFAULT 0,
            user_dust INT NOT NULL DEFAULT 0
        );
    """)        # TODO: how to implement deck_id? Hash?

