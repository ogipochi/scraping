from mysql_db import TwitterDB
from twitter_scraper import TwitterScraper
import time
import os
import sys
import logging

"""
第一引数にスクロール数を受け取る
"""

search_tweet = ['為替','exchange','money order','dollar','rate','yen','euro','economics','経済','ドル']



args = sys.argv
logger = logging.getLogger()
twitter_scraper = TwitterScraper()
twitter_scraper.open_browser()
twitter_scraper.logout()
twitter_scraper.login()
twitter_db = TwitterDB()
twitter_db.create_table('twitter_db')

while True:
    keyword = twitter_db.exec_cmd('SELECT keyword FROM query;')
    if keyword:
        search_tweet = keyword
    for q in search_tweet:
        for result in twitter_scraper.search_tweet(q,int(args[1]))
            twitter_db.add_record(result,'twitter_db',q)
            twitter_db.commit()
        time.sleep(10)
    



