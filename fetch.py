import datetime
import sqlite3

import tweepy

import config
import utils

def is_clean(status):
    return (not '@' in status.text) \
            and (not 'RT' in status.text.lower()) \
            and (not 't.co' in status.text.lower()) \
            and (not 'simulator' in status.author.screen_name.lower()) \
            and (not 'SolideSchlange' in status.author.screen_name)

def latest_tweet_id():
    db_connection = sqlite3.connect(config.SQLITE_DB)
    db_cursor = db_connection.cursor()
    db_cursor.execute('SELECT * FROM tweets WHERE id=(SELECT max(id) FROM tweets)')
    res = db_cursor.fetchone()
    db_connection.close()
    return res[2]

def fetch_tweets():
    api = utils.get_api()

    statuses = api.home_timeline(count=100, since_id=latest_tweet_id())

    db_connection = sqlite3.connect(config.SQLITE_DB)
    db_cursor = db_connection.cursor()

    for status in filter(is_clean, statuses):
        print(status.author.screen_name)
        print(status.text)
        print(status.created_at)
        print(type(status.created_at))
        print()
        db_cursor.execute(
            'INSERT INTO tweets VALUES (?,?,?,?)',
            (
                status.author.screen_name,
                status.text,
                status.id,
                status.created_at.timestamp(),
            )
        )

    db_connection.commit()
    db_connection.close()

if __name__ == '__main__':
    fetch_tweets()
    #print(latest_tweet_id())