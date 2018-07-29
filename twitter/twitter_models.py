
from datetime import datetime

class SearchGroup():
    def __init__(self,group_name,id=None):
        self.group_name = group_name
        self.id = id
class SearchQuery():
    def __init__(self,keyword,group_id = None,id=None):
        self.keyword = keyword
        self.group_id = group_id
        self.id = id
class Tweet():
    def __init__(self,tweet_id,tweet_text,user_id,tweet_time,
    search_query_id=0,conversation_id=0,retweet_count=0,reply_count=0,
    favo_count=0,to_reply_id=None,id=None,tbl_name="tweet"):
        self.tweet_id = tweet_id
        self.tweet_text = self.escape_quates(tweet_text)
        self.user_id = user_id
        self.tweet_time = datetime.strptime(tweet_time.replace(".000Z",""),"%H:%M - %Y年%m月%d日")
        self.conversation_id = conversation_id
        self.retweet_count = self.cut_punctuation(retweet_count)  # 千単位で入るカンマが邪魔なので先に削除
        self.reply_count = self.cut_punctuation(reply_count)      # 千単位で入るカンマが邪魔なので先に削除
        self.favo_count = self.cut_punctuation(favo_count)        # 千単位で入るカンマが邪魔なので先に削除
        self.search_query_id = search_query_id
        self.id=id
        self.tbl_name = tbl_name
    def escape_quates(self,text):
        text = text.replace('"','\"')
        text = text.replace("'","\'")
        return text
    def cut_punctuation(self,text):
        text = text.replace(',','')
        text = text.replace('、','')
        text = text.replace('.','')
        text = text.replace('。','')
        return text
    def sql_create_tbl(self):
        """
        テーブル作成のためのSQL文
        """
        script = (
            "CREATE TABLE " + self.tbl_name + 
            " (id integer NOT NULL AUTO_INCREMENT,"
            "tweet_id char(63) ,"
            "tweet_text text ," 
            "user_id char(31) ,"
            "tweet_time datetime ,"
            "conversation_id char(31) ,"
            "retweet_count integer ,"
            "reply_count integer ,"
            "favo_count integer ,"
            "search_query_id integer ,"
            "obtained datetime ,"
            "PRIMARY KEY (id));"
        )
        return script
    def sql_add_bulk_prefix(self):
        script =("INSERT INTO " + self.tbl_name + 
            " (tweet_id , tweet_text , user_id , tweet_time ," + 
            "conversation_id , retweet_count , reply_count ," + 
            "favo_count, search_query_id , obtained ) VALUES ")
        return script
    def sql_add_bulk(self):
        """
        バルクインサートするためのSQL文
        """
        script = (
            "('{tweet_id}' , '{tweet_text}' , '{user_id}' ,'{tweet_time}' ,"
            "'{conversation_id}' , {retweet_count} , {reply_count} , "
            "{retweet_count} , {search_query_id} , '{obtained}')".format(
                tweet_id=self.tweet_id,
                tweet_text = self.tweet_text,
                user_id = self.user_id,
                tweet_time = self.tweet_time,
                conversation_id = self.conversation_id,
                retweet_count = self.retweet_count,
                reply_count=self.reply_count,
                favo_count = self.favo_count,
                search_query_id = self.search_query_id,
                obtained = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            ))
        return script
    def sql_search_same_record(self):
        script = ("SELECT * FROM {tbl_name}"
        " WHERE tweet_id='{tweet_id}' AND user_id='{user_id}';".format(
            tbl_name=self.tbl_name,
            tweet_id = self.tweet_id,
            user_id=self.user_id
        )) 
        return script
    
    


class User:
    """
    ユーザー管理のクラ
    """
    def __init__(self,user_id,username,is_active=True,tbl_name='user'):
        self.user_id = user_id
        self.username = username
        self.is_active=is_active
        self.tbl_name=tbl_name
    def home_url(self):
        url = "https://twitter.com/" + self.username
        return url
    def following_list_url(self):
        url = "https://mobile.twitter.com/" + self.username + '/following'
        return url
    def sql_create_tbl(self):
        """
        テーブル作成のためのSQL文
        """
        script = (
            "CREATE TABLE " + self.tbl_name + 
            " (id integer NOT NULL AUTO_INCREMENT,"
            "user_id char(63) ,"
            "username char(63) ,"
            "is_active boolean DEFAULT true ," 
            "PRIMARY KEY (id));"
        )
        return script
    def sql_add_bulk_prefix(self):
        script =("INSERT INTO " + self.tbl_name + 
            " (user_id , username , is_active ) VALUES ")
        return script
    def sql_add_bulk(self):
        """
        バルクインサートするためのSQL文
        """
        script = (
            "('{user_id}' , '{username}' , {is_active})".format(
                user_id=self.user_id,
                username = self.username,
                is_active = self.is_active))
        return script
    def sql_search_same_record(self):
        script = ("SELECT * FROM {tbl_name}"
        " WHERE user_id='{user_id}';".format(
            tbl_name=self.tbl_name,
            user_id=self.user_id
        )) 
        return script

class UserRelation():
    """
    ユーザーのフォロー関係のみを示すクラス
    """
    def __init__(self,user_id,follower_id):
        self.user_id = user_id
        self.follower_id = follower_id
    