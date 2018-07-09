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
twitter_db.create_table('twitter')
while True:
    for q in search_tweet:
        search_results = twitter_scraper.search_tweet(q,args[1])
        for search_result in search_results:
            twitter_db.add_record(search_result,'twitter',q)
        logger.info(q,'is finised...exceed...')
        time.sleep(10)
    



