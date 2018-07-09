from mysql_db import TwitterDB
from twitter_scraper import TwitterScraper
import time
import os

search_tweet = ['為替','exchange','money order','dollar','rate','yen','euro','economics','経済','ドル']

twitter_scraper = TwitterScraper()
twitter_scraper.open_browser()
twitter_scraper.logout()
twitter_scraper.login()
twitter_db = TwitterDB()
twitter_db.create_table('twitter')
while True:
    for q in search_tweet:
        search_result = twitter_scraper.search_tweet(q,500)
        twitter_db.add_record(search_result,'twitter',q)
    



