import psycopg2

user_password = input('Enter password: ')

with psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password=user_password) as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams(
            team_id SERIAL PRIMARY KEY,
            team_name VARCHAR ( 50 ) UNIQUE NOT NULL,
            team_link VARCHAR ( 255 ) UNIQUE NOT NULL            
        );
        CREATE TABLE IF NOT EXISTS players(
            player_id SERIAL PRIMARY KEY,
            name VARCHAR ( 50 ) NOT NULL,
            player_link VARCHAR ( 255 ) UNIQUE NOT NULL,
            role VARCHAR ( 8 ),
            player_number INT,
            team_id INT,
            FOREIGN KEY (team_id)
                REFERENCES teams (team_id)
        );
        CREATE TABLE IF NOT EXISTS tournaments(
            t_id SERIAL PRIMARY KEY,
            t_name varchar ( 50 ) NOT NULL
        );
        CREATE TABLE IF NOT EXISTS stats(
            player_id INT NOT NULL,
            t_id INT NOT NULL,
            FOREIGN KEY (player_id)
                REFERENCES players (player_id),
            FOREIGN KEY (t_id)
                REFERENCES tournaments (t_id),
            n_games INT NOT NULL,
            pts INT NOT NULL,
            goals INT NOT NULL,
            assists INT NOT NULL,
            penalty_time INT NOT NULL
        );  
    """)

