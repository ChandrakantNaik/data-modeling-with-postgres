# DROP TABLES

songplay_table_drop = "DROP TABLE songplays"
user_table_drop = "DROP TABLE users"
song_table_drop = "DROP table songs"
artist_table_drop = "DROP table artists"
time_table_drop = "DROP table time"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays 
    (   songplay_id SERIAL PRIMARY KEY NOT NULL, 
        start_time TIMESTAMP NOT NULL, 
        user_id INT NOT NULL, 
        song_id VARCHAR, 
        artist_id VARCHAR, 
        session_id INT, 
        level VARCHAR, 
        location VARCHAR,
        user_agent VARCHAR
    );
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users
    (
        user_id INT PRIMARY KEY NOT NULL,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR(1),
        level VARCHAR
    );
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs 
    (
        song_id VARCHAR PRIMARY KEY NOT NULL, 
        title VARCHAR NOT NULL, 
        artist_id VARCHAR NOT NULL, 
        year INT, 
        duration NUMERIC NOT NULL
    );
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists 
    (
        artist_id VARCHAR PRIMARY KEY NOT NULL, 
        name VARCHAR NOT NULL, 
        location VARCHAR, 
        latitude double precision, 
        longitude double precision);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time
    (
        start_time TIMESTAMP PRIMARY KEY NOT NULL,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT,
        weekday INT
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, song_id, artist_id, session_id, level, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING;
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET
    (first_name, last_name, gender, level) = (EXCLUDED.first_name, EXCLUDED.last_name, EXCLUDED.gender,EXCLUDED.level);
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO UPDATE SET
    (title, artist_id, year, duration) = (EXCLUDED.title, EXCLUDED.artist_id, EXCLUDED.year,EXCLUDED.duration);
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO UPDATE SET
    (name, location, latitude, longitude) = (EXCLUDED.name, EXCLUDED.location, EXCLUDED.latitude,EXCLUDED.longitude);
""")


time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (start_time) DO UPDATE SET
    (hour, day, week, month, year, weekday) = (EXCLUDED.hour, EXCLUDED.day, EXCLUDED.week,EXCLUDED.month,EXCLUDED.year,EXCLUDED.weekday);
""")

# FIND SONGS

song_select = ("""
Select distinct songs.song_id, artists.artist_id 
From songs 
INNER JOIN artists 
on songs.artist_id = artists.artist_id
Where songs.title = %s 
And artists.name =  %s
And songs.duration = %s 
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]