class TwitterDB:
    
    def __init__(self,host=None,user=None,pswd=None,db_name=None,port=3306):
        import mysql.connector
        import logging
        import os

        self.host = host or os.getenv("SQL_HOST") 
        self.user = user or os.getenv("SQL_USER")
        self.pswd = pswd or os.getenv("SQL_PSWD")
        self.db_name = db_name or os.getenv("SQL_DBNAME")
        self.port = port or 3306
        
        self.conn = mysql.connector.connect(     # Mysqlへのコネクタ
            host = self.host,                 
            port = self.port,                 
            user = self.user,
            password=self.pswd,
            database = self.db_name)
        self.logger = logging.getLogger()        # ログ出力用logger
        # 接続できていない場合再接続
        if self.conn.is_connected==False:
            self.reconnect()
        
    def reconnect(self):
        """
        再接続後接続確認し,
        失敗した場合log出力
        """
        self.conn.ping(reconnect=True)
        if self.conn.is_connected()==False:
            self.logger.error("not connected MySQL...\n"
                              "host     : {host}\n"
                              "port     : {port}\n"
                              "user     : {user}\n"
                              "password : {pswd}\n"
                              "database : {db}\n"
                             "Please Check!!!".format(
                                 host=self.host,
                                 port = self.port,
                                 user = self.user,
                                 pswd=self.pswd,
                                 db_name = self.db_name))
            return False
        else:
            self.logger.info("connection is living now...")
            return True
    def exec_cmd(self,cmd,fetch=False):
        """
        接続の確認後コマンド実行
        """
        
        # 再接続
        self.reconnect()
        self.cur = self.conn.cursor()
        try:
            self.cur.execute(cmd)
        except:
            return False
        if fetch:
            return self.cur.fetchall()
        
    def create_table(self,tbl_name):
        # テーブル名を受取り,テーブルの作成を行う
        # 指定されたテーブル名のテーブルがすでに存在する場合は
        # Falseを返す
        if self.confirm_table_exist(tbl_name):
            self.logger.info('{} Table already exists...'.format(tbl_name))
            return False
        script = ("CREATE TABLE " + tbl_name + 
                  " (SID integer ," +
                  " TweetID char(64) ,"+
                  " UserName char(64) ,"+
                  " UserID char(32) ," +
                  " ConversationID char(32) ," +
                  " TweetTime char(32) ," + 
                  " TweetText text ," +
                  " Favorite char(16) ," + 
                  " Reply char(16) ," + 
                  " Retweet char(16) ," + 
                  " SearchQuery char(32) ," + 
                  " Obtained datetime);"
                 )
        
        self.exec_cmd(script)
        return True
    def confirm_table_exist(self,tbl_name):
        # テーブル名を受取り,その名前のテーブルが存在するか否かをBool型で返す
        script = (
            "SHOW TABLES FROM " + self.db_name +
            " LIKE '"+tbl_name +  "'")
        result = self.exec_cmd(script,True)
        
        if len(result) == 0:
            return False
        else:
            return True
    def add_record(self,data_dict,tbl_name,search_q=""):
        """
        データレコードの追加
        後々の管理のためにsearch_qも保存しておく

        data_dict　辞書型
        tweet_id   : ツイートid(str)
        username   : @以下ユーザ名(str)
        conversation_id : 会話id(str)    
        user_id    : ユーザid(str)
        tweet_time : ツイート日時(str)
        tweet_text : 結ーとテキスト(str)
        favorite   : いいね数(str)
        reply      : 返信数(str)
        retweet    : リツイート数(str)

        """
        
        from datetime import datetime,date,timedelta
        # エスケープ
        for key in data_dict:
            data_dict[key] = data_dict[key].translate(str.maketrans({"'":  r"\'",'"':  r'\"'}))
        
        self.create_table(tbl_name)
        # レコードがすでに存在する場合終了
        if self.exist_record(data_dict,tbl_name):
            print('already record exist... skip...')
            return False 
        script = ("INSERT INTO " + tbl_name + 
                  " (TweetID , UserName , UserID ,ConversationID , TweetTime , TweetText ," 
                  " Favorite , Reply , Retweet , SearchQuery , Obtained ) "
                  "VALUES ('{tweet_id}' , '{username}' , '{user_id}' , '{conversation_id}' ," 
                  "'{tweet_time}' , '{tweet_text}' , '{favorite}' , '{reply}' ," 
                  "'{retweet}' ,'{search_q}' , '{now}');".format(
                      tweet_id = data_dict["tweet_id"],
                      username = data_dict["username"],
                      user_id = data_dict["user_id"],
                      conversation_id = data_dict["conversation_id"],
                      tweet_time = data_dict["tweet_time"],
                      tweet_text = data_dict["tweet_text"],
                      favorite = data_dict["favorite"],
                      reply = data_dict["reply"],
                      retweet = data_dict["retweet"],
                      search_q = search_q,
                      now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                  )
        )
        self.exec_cmd(script)
        print('[EXECUTE]',sql)
        self.logger.info('[SQL-COMP]',script)
        return True
    def exist_record(self,data_dict,tbl_name):
        """
        レコードが存在する場合Trueを返す
        """
        script = (
            "SELECT * FROM {tbl_name} "
            "WHERE UserID='{user_id}' AND TweetID ='{tweet_id}';".format(
                tbl_name = tbl_name,
                user_id = data_dict["user_id"],
                tweet_id = data_dict["tweet_id"]
            ))
        result = self.exec_cmd(script,True)
        if len(result)==0:
            return False
        else:
            print(result)
            return True
    def show_all_record(self,tbl_name):
        """
        すべてのレコードを返す.
        """
        script = ("SELECT * FROM {tbl_name};".format(tbl_name=tbl_name))
        result = self.exec_cmd(script,True)
        return result
    def close(self):
        self.cur.close()
        self.conn.close()
    def commit(self):
        self.conn.commit()
        
        
        
        