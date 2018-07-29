from general import MySql
from twitter_models import *
from scraper import TwitterScraper
import time
import os

class Collector:
    def __init__(self):
        self.mysql_django = MySql(
            host = os.getenv('SQL_DNG_HOST'),
            user=os.getenv('SQL_DNG_USER'),
            pswd=os.getenv('SQL_DNG_PSWD'),
            db_name=os.getenv('SQL_DNG_DBNAME'),
            port=3306)
        self.mysql_db = MySql(
            host = os.getenv('SQL_DB_HOST'),
            user=os.getenv('SQL_DB_USER'),
            pswd=os.getenv('SQL_DB_PSWD'),
            db_name=os.getenv('SQL_DB_DBNAME'),
            port=3306)
        self.twitter = TwitterScraper()
    def get_search_junre(self):
        junre_list = self.mysql_django.exec_cmd('SELECT DISTINCT id,name FROM twitter_junre;',fetch=True)
        for junre in junre_list:
            yield junre
    def get_search_query(self,junre_id):
        query_list = self.mysql_django.exec_cmd('SELECT keyword FROM twitter_query WHERE junre_id={junre_id};'.format(junre_id=junre_id),fetch=True)
        for query in query_list:
            yield query[0]
    def get_data(self,query):
        self.twitter.open_browser()
        self.twitter.logout()
        self.twitter.login(os.getenv('TWITTER_EMAIL'),os.getenv('TWITTER_PSWD'))
        for tweet in self.twitter.search_tweet(q=query,scroll=1):
            yield tweet
        self.twitter.quit_browser()
    def collect(self,query):
        counter_tweet = 0
        counter_user = 0
        exec_script_tweet = ""
        exec_script_user = ""
        first_iteration_tweet = True
        first_iteration_user = True
        for user,tweet in self.get_data(query):
            print('    sql add counter [tweet]{}'.format(counter_tweet))
            print('    sql add counter [user]{}'.format(counter_user))
            same_tweet_exist = self.mysql_db.exec_cmd(tweet.sql_search_same_record(),True)
            same_user_exist = self.mysql_db.exec_cmd(user.sql_search_same_record(),True)
            
            #　すでにレコードが存在する場合スキップ
            if len(same_tweet_exist)==0:
                if first_iteration_tweet:
                    self.mysql_db.exec_cmd(tweet.sql_create_tbl())
                    exec_script_tweet += tweet.sql_add_bulk_prefix() + tweet.sql_add_bulk()
                    counter_tweet+=1
                    first_iteration_tweet=False
                else:
                    exec_script_tweet += ',' + tweet.sql_add_bulk()
                    counter_tweet+=1
            if len(same_user_exist)==0:
                if first_iteration_user:
                    self.mysql_db.exec_cmd(user.sql_create_tbl())
                    exec_script_user += user.sql_add_bulk_prefix() + user.sql_add_bulk()
                    counter_user += 1
                    first_iteration_user = False
                else:
                    exec_script_user += ',' + user.sql_add_bulk()
                    counter_user += 1        
            continue
        exec_script_tweet += ';'
        exec_script_user += ';'
        print("insert {} tweet...".format(counter_tweet))
        self.mysql_db.exec_cmd(exec_script_tweet)
        print("insert {} user...".format(counter_user))
        self.mysql_db.exec_cmd(exec_script_user)
        return True
    def exec_collect(self):
        for junre in self.get_search_junre():
            print('load junre : {}'.format(junre[1]))
            for search_query in self.get_search_query(junre[0]):
                print('start search : {}'.format(search_query))
                self.collect(search_query)
        return True

collector = Collector()
while True:
    try:
        collector.exec_collect()
    except Exception as e:
        print('Error [{error}]]'.format(error=e))
        time.sleep(300)

    
            



