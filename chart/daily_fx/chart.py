from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, os
from datetime import datetime
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Chrome,ChromeOptions
import logging


class DairyFxChartScraper:
    def __init__(self,separate=22,span=4,url='https://www.dailyfx.com/forex-rates'):
        """
        span : ページ読み込み待機時の秒数
        """
        self.span = span
        self.logger = logging.getLogger()
        self.url = url
        self.separate=separate
    def open_browser(self):
        """
        ブラウザを開いて最大画面にして待機
        """
        options = ChromeOptions()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
    def quit_browser(self):
        """
        ブラウザを終了
        メモリを開放するために必ず呼ぶ
        """
        self.browser.quit()
    def access(self):
        self.browser.get(self.url)
        time.sleep(self.span)
        return True
    def get_info_as_list(self,order=0):
        """
        情報を取得.
        """
        info_list = []
        rate_rows = self.browser.find_elements_by_css_selector('tr.rates-row')
        for rate_row in rate_rows:
            data_dict = dict()
            data_dict["symbol"] = rate_row.get_attribute('id')
            data_dict["bid"] = rate_row.find_element_by_css_selector('td.text-right.rates-row-td span[data-type="bid"]').get_attribute('data-value')
            data_dict["ask"] = rate_row.find_element_by_css_selector('td.text-right.rates-row-td span[data-type="ask"]').get_attribute('data-value')
            data_dict["spread"] =   rate_row.find_element_by_css_selector('td.text-right.rates-row-td span[id*="-spread"]').text
            data_dict["datetime"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            
            info_list.append(data_dict)
        return info_list
