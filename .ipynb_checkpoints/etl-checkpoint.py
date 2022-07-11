import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
        read the songs data json files, insert data into songs & artist table
        param cur: cursor object of the connection object used to execute CRUD statements. 
        param filepath: json filepath of songs data
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']]
    song_data = tuple(x for x in song_data.values.tolist()[0])
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']]
    artist_data = tuple(x for x in artist_data.values.tolist()[0])
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
        read the log json files, insert data into users, time and songplays table
        param cur: cursor object of the connection object used to execute CRUD statements. 
        param filepath: json filepath of logs data
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong']
    df.reset_index(drop=True)

    # convert timestamp column to datetime
    t = pd.Series(pd.to_datetime(df['ts'], unit='ms'))
    df['ts'] = df['ts'].apply(lambda x: pd.to_datetime(x, unit='ms'))
    
    # insert time data records
    time_data = (list(zip(list(t), list(t.dt.hour), list(t.dt.day), list(t.dt.week), list(t.dt.month), list(t.dt.year), list(t.dt.weekday))))
    column_labels = ['ts', 'year', 'month', 'day', 'hour', 'week_of_day', 'week_of_year']
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates().reset_index(drop=True)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, songid, artistid, row.sessionId, row.level, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
        get all the files and called the process_log_file or process_song_file func.
        param cur: cursor object of the connection object used to execute CRUD statements.
        param conn: connection object returned.
        param filepath: songs or logs data filepath.
        param func: process_log_file or process_song_file function.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
        main functions establishes connection to database and create a cursor.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()