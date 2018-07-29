import mysql.connector
import logging
import os

class MySql:
    def __init__(self,host=None,user=None,pswd=None,db_name=None,port=3306):
        

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
                              "database : {db_name}\n"
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
    def close(self):
        self.cur.close()
        self.conn.close()
    def commit(self):
        self.conn.commit()
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
    def show_all_record(self,tbl_name):
        """
        すべてのレコードを返す.
        """
        script = ("SELECT * FROM {tbl_name};".format(tbl_name=tbl_name))
        result = self.exec_cmd(script,True)
        return result