from mysql_db import ChartDB
from chart import DairyFxChartScraper
import time,os,sys,logging
import multiprocessing


iteration = 100
span_time=0

daily_fx_chart_scraper = DairyFxChartScraper()
daily_fx_chart_scraper.open_browser()
daily_fx_chart_scraper.access()
chart_db = ChartDB()
chart_db.create_table('daily_fx')

def save(info_list):
    for info_dict in info_list:
        chart_db.add_record(info_dict,'daily_fx')
    return True
while True:
    info_list = []
    for i in range(iteration):
        # 計測開始
         
        info_list.append(daily_fx_chart_scraper.get_info_as_list())
    print(info_list[0]["datetime"])
    p = multiprocessing.Process(target=save,args=(info_list,))
    p.start()

