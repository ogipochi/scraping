from mysql_db import ChartDB
from chart import DairyFxChartScraper
import time,os,sys,logging
import threading
from mysql.connector.errors import OperationalError
from datetime import dateitme


iteration = 10
first_inuse = False
second_inuse = False
third_inuse = False
forth_inuse = False
span_time=10
span_increment = 1
span_rate_of_change = 0.96

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
chart_db_first.create_table('daily')
chart_db_second = ChartDB(
    host=host_2,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_second.create_table('daily')

chart_db_third = ChartDB(
    host=host_3,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_third.create_table('daily')

chart_db_forth = ChartDB(
    host=host_4,
    user=user,
    pswd=pswd,
    db_name=db_name
)
chart_db_forth.create_table('daily')

def save_first(info_list):
    """
    INSERT権限を渡されて,すべてのデータを格納するまで繰り返す
    待ち回数が増えるたびにspan_timeをインクリメント
    """
    global span_time
    global first_inuse
    global span_increment
    global span_rate_of_change
    while True:
        if first_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            first_inuse = True
            for info_dict in info_list:
                chart_db_first.add_record(info_dict,'daily')
            break
    chart_db_first.commit()
    first_inuse = False

    return True

def save_second(info_list):
    global span_time
    global second_inuse
    global span_increment
    global span_rate_of_change
    while True:
        if second_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            second_inuse = True
            
            for info_dict in info_list:
                chart_db_second.add_record(info_dict,'daily',False)
            break
    chart_db_second.commit()
    second_inuse = False
    return True

def save_third(info_list):
    global span_time
    global third_inuse
    global span_increment
    global span_rate_of_change
    while True:
        if third_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            third_inuse = True
            for info_dict in info_list:
                chart_db_third.add_record(info_dict,'daily',False)
            break
    chart_db_third.commit()
    third_inuse = False
    return True

def save_forth(info_list):
    global span_time
    global forth_inuse
    global span_increment
    global span_rate_of_change
    while True:
        if forth_inuse:
            span_increment = span_increment * span_rate_of_change
            span_time += span_increment
            print('[{time}]span_time={span}'.format(time=datetime.now(),span=span_time))
            time.sleep(span_time)
            continue
        else:
            forth_inuse = True
            for info_dict in info_list:
                chart_db_forth.add_record(info_dict,'daily',False)
            break
    chart_db_forth.commit()
    forth_inuse = False
    return True





while True:
    info_list = []
    for i in range(iteration):
        info_list.extend(daily_fx_chart_scraper.get_info_as_list())
        time.sleep(span_time)
    print(info_list[0])
    th = threading.Thread(target=save_first,kwargs = {'info_list':info_list})
    th.start()
    info_list = []
    for i in range(iteration):
        info_list.extend(daily_fx_chart_scraper.get_info_as_list())
        time.sleep(span_time)
    print(info_list[0])
    th = threading.Thread(target=save_second,kwargs={'info_list':info_list})
    th.start()

    for i in range(iteration):
        info_list.extend(daily_fx_chart_scraper.get_info_as_list())
        time.sleep(span_time)
    print(info_list[0])
    th = threading.Thread(target=save_third,kwargs={'info_list':info_list})
    th.start()

    for i in range(iteration):
        info_list.extend(daily_fx_chart_scraper.get_info_as_list())
        time.sleep(span_time)
    print(info_list[0])
    th = threading.Thread(target=save_forth,kwargs={'info_list':info_list})
    th.start()