from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from twitter_models import User,SearchGroup,SearchQuery,Tweet
from selenium.webdriver import Chrome,ChromeOptions

class TwitterScraper:
    """ツイッタースクレイピング用クラス"""
    def __init__(self,span=2,):
        """
        span : ページ読み込み待機時の秒数
        """
        self.span = span
    def open_browser(self):
        """
        ブラウザを開いて最大画面にして待機
        """
        options = ChromeOptions()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser.maximize_window()
        print('open browser')
    def quit_browser(self):
        """
        ブラウザを終了
        メモリを開放するために必ず呼ぶ
        """
        self.browser.quit()
        print('quit browser')
    def logout(self):
        """
        ログアウト
        """
        self.browser.get("https://twitter.com/logout")
        time.sleep(self.span)
        print('logout twitter account')
    def scroll(self,scroll=10):
        for i in range(scroll):
            actions = ActionChains(self.browser)
            actions.send_keys(Keys.END)
            actions.perform()
            time.sleep(self.span)
    def login(self,email=None,password=None):
        """
        Twitterのログイン
        email    : Twitterアカウント登録アドレス
        password : Twitterアカウント登録パスワード
        """
        self.browser.get("https://twitter.com/login")
        time.sleep(self.span)
        input_email = self.browser.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[1]/input')
        input_password = self.browser.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/fieldset/div[2]/input')
        input_email.send_keys(email or os.getenv('TWITTER_EMAIL'))
        input_password.send_keys(password or os.getenv('TWITTER_PSWD'))
        submit_button = self.browser.find_element_by_xpath('//*[@id="page-container"]/div/div[1]/form/div[2]/button')
        submit_button.click()
        print('login twitter : {email}'.format(email = (email or os.getenv('TWITTER_EMAIL'))))
    def search_tweet(self,q='',scroll=20):
        """
        検索ワードを受け取ってツイート情報のリストを返す
        メソッド引数
        q           : 検索ワード
        scroll      : 検索結果の読み取りの量
        
        リターン(辞書内包のリスト型)
        """
        print('start search tweet with query "{q}" and scroll num {scroll}'.format(q=q,scroll=scroll))
        
        # serchboxの取得とクエリ送信送信
        self.browser.get("https://twitter.com/search?f=tweets&vertical=news&q="+ q + "&src=typd")
        time.sleep(self.span)
        
        # 指定された回数スクロール
        for i in range(scroll):
            print('    scroll count {count}'.format(count=i))
            actions = ActionChains(self.browser)
            actions.send_keys(Keys.END)
            actions.perform()
            time.sleep(self.span)
        # ツイートストリームの取得
        tweet_list = self.browser.find_element_by_css_selector('#stream-items-id')
        tweet_cards = tweet_list.find_elements_by_css_selector('li.js-stream-item.stream-item.stream-item[data-item-type="tweet"]')
        print('    start extracting tweet ')
        tweet_info_dict_list = []
        for tweet_card in tweet_cards:
            
            tweet_info_dict = dict()
            
            tweet_id = tweet_card.get_attribute("data-item-id")
            
            content = tweet_card.find_element_by_css_selector('div.content')
            username = content.find_element_by_css_selector('.username').text
            text = content.find_element_by_css_selector('p.TweetTextSize.js-tweet-text.tweet-text').text
            tweet_time = content.find_element_by_css_selector('small.time a.tweet-timestamp').get_attribute('title')
            conversation_id = content.find_element_by_css_selector('small.time a.tweet-timestamp').get_attribute('data-conversation-id')
            user_id = content.find_element_by_css_selector('.stream-item-header a.account-group').get_attribute('data-user-id')
            action_retweet = content.find_element_by_css_selector('button.ProfileTweet-actionButton.js-actionButton.js-actionRetweet').text.split('リツイート')[-1]
            action_reply = content.find_element_by_css_selector('button.ProfileTweet-actionButton.js-actionButton.js-actionReply').text.split('返信')[-1]
            action_favorite = content.find_element_by_css_selector('button.ProfileTweet-actionButton.js-actionButton.js-actionFavorite').text.split('いいね')[-1]
            tweet_data = content.find_element_by_css_selector('span._timestamp.js-short-timestamp')
            
            tweet = Tweet(
                tweet_id=tweet_id,
                tweet_text=text,
                user_id = user_id,
                tweet_time=tweet_time,
                conversation_id=conversation_id,
                retweet_count=action_retweet.split('\n')[-1] or "0",
                reply_count=action_reply.split('\n')[-1] or "0",
                favo_count=action_favorite.split('\n')[-1] or "0",
            )
            user = User(
                user_id=user_id,
                username=username
            )
            yield user,tweet
            # tweet_info_dict["tweet_id"] = tweet_id
            # tweet_info_dict["username"] = username
            # tweet_info_dict["tweet_time"] = tweet_time
            # tweet_info_dict["user_id"] = user_id
            # tweet_info_dict["conversation_id"] = conversation_id
            # tweet_info_dict["retweet"] = action_retweet.split('\n')[-1]
            # tweet_info_dict["reply"] = action_reply.split('\n')[-1]
            # tweet_info_dict["favorite"] = action_favorite.split('\n')[-1]
            # tweet_info_dict["tweet_text"] = text
            # tweet_info_dict_list.append(tweet_info_dict)
        
        # return tweet_info_dict_list