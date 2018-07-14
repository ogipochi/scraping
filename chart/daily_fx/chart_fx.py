from mysql_db import ChartDB
from chart import DairyFxChartScraper
import time,os,sys,logging
import threading
from mysql.connector.errors import OperationalError
from datetime import datetime


iteration = 10
first_inuse = False
second_inuse = False
third_inuse = False
forth_inuse = False
span_time=3
span_increment = 1
span_rate_of_change = 0.96
tbl_name = 'daily'

host_1 = os.getenv('SQL_HOST_1')
host_2 = os.getenv('SQL_HOST_2')
host_3 = os.getenv('SQL_HOST_3')
host_4 = os.getenv('SQL_HOST_4')



user = os.getenv('SQL_USER')
pswd = os.getenv('SQL_PSWD')
db_name = os.getenv('SQL_DBNAME')

daily_fx_chart_scraper = DairyFxChartScraper()
daily_fx_chart_scraper.open_browser()
daily_fx_chart_scraper.access()
chart_db_first = ChartDB(
    host=host_1,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_first.create_table(tbl_name)
chart_db_second = ChartDB(
    host=host_2,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_second.create_table(tbl_name)

chart_db_third = ChartDB(
    host=host_3,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_third.create_table(tbl_name)

chart_db_forth = ChartDB(
    host=host_4,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_forth.create_table(tbl_name)

def save_first(script):
    """
    INSERT権限を渡されて,すべてのデータを格納するまで繰り返す
    待ち回数が増えるたびにspan_timeをインクリメント
    """
    global span_time
    global first_inuse
    global span_increment
    global span_rate_of_change
    global chart_db_first
    while True:
        if first_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            first_inuse = True
            chart_db_first.exec_cmd(script)
            break
    chart_db_first.commit()
    first_inuse = False

    return True

def save_second(script):
    global span_time
    global second_inuse
    global span_increment
    global span_rate_of_change
    global chart_db_second
    while True:
        if second_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            second_inuse = True
            
            chart_db_second.exec_cmd(script)
            break
    chart_db_second.commit()
    second_inuse = False
    return True

def save_third(script):
    global span_time
    global third_inuse
    global span_increment
    global span_rate_of_change
    global chart_db_third
    while True:
        if third_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            third_inuse = True
            chart_db_forth.exec_cmd(script)
            break
    chart_db_third.commit()
    third_inuse = False
    return True

def save_forth(script):
    global span_time
    global forth_inuse
    global span_increment
    global span_rate_of_change
    global chart_db_forth
    while True:
        if forth_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            forth_inuse = True
            chart_db_forth.exec_cmd(script)
            break
    chart_db_forth.commit()
    forth_inuse = False
    return True



def script_addition_construst(data_list):
    script_addition = ""
    for data_dict in data_list:
        script_addition+="('{symbol}' , '{bid}' , '{ask}' , '{spread}' , '{datetime}') ,".format(
                    symbol = data_dict["symbol"],
                    bid = data_dict["bid"],
                    ask = data_dict["ask"],
                    spread = data_dict["spread"],
                    datetime = data_dict["datetime"],)
    return script_addition



while True:
    script = "INSERT INTO " + tbl_name + " (symbol , bid , ask , spread , obtained ) VALUES "
    for i in range(iteration):
        # すべてのデータを取得
        data_list = daily_fx_chart_scraper.get_info_as_list()
        
        script += script_addition_construst(data_list)
    script_list = list(script)
    script_list[-1] = ";"
    script = "".join(script_list)
    print('thread start')
    print(script)
    th = threading.Thread(target=save_first,kwargs = {'script':script})
    th.start()
    script = "INSERT INTO " + tbl_name + " (symbol , bid , ask , spread , obtained ) VALUES "
    for i in range(iteration):
        # すべてのデータを取得
        data_list = daily_fx_chart_scraper.get_info_as_list()
        
        script += script_addition_construst(data_list)
    script_list = list(script)
    script_list[-1] = ";"
    script = "".join(script_list)
    print('thread start')
    th = threading.Thread(target=save_second,kwargs = {'script':script})
    th.start()


    script = "INSERT INTO " + tbl_name + " (symbol , bid , ask , spread , obtained ) VALUES "
    for i in range(iteration):
        # すべてのデータを取得
        data_list = daily_fx_chart_scraper.get_info_as_list()
        
        script += script_addition_construst(data_list)
    script_list = list(script)
    script_list[-1] = ";"
    script = "".join(script_list)
    print('thread start')
    th = threading.Thread(target=save_second,kwargs = {'script':script})
    th.start()

    script = "INSERT INTO " + tbl_name + " (symbol , bid , ask , spread , obtained ) VALUES "
    for i in range(iteration):
        # すべてのデータを取得
        data_list = daily_fx_chart_scraper.get_info_as_list()
        
        script += script_addition_construst(data_list)
    script_list = list(script)
    script_list[-1] = ";"
    script = "".join(script_list)
    print('thread start')
    th = threading.Thread(target=save_forth,kwargs = {'script':script})
    th.start()