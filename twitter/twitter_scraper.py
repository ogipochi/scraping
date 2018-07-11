from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.webdriver import Chrome, ChromeOptions
import logging
class TwitterScraper:
    """ツイッタースクレイピング用クラス"""
    def __init__(self,span=4,):
        """
        span : ページ読み込み待機時の秒数
        """
        self.span = span
        self.logger = logging.getLogger()
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
    def logout(self):
        """
        ログアウト
        """
        self.browser.get("https://twitter.com/logout")
        time.sleep(self.span)
    def scroll(self,scroll=10):
        for i in range(scroll):
            try:
                actions = ActionChains(self.browser)
                actions.send_keys(Keys.END)
                actions.perform()
                time.sleep(self.span)
            except TimeoutException:
                return 
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
        time.sleep(3)
        print(self.browser.current_url)
        print(self.browser.page_source)
    def search_tweet(self,q='',scroll=20):
        """
        検索ワードを受け取ってツイート情報のリストを返す
        メソッド引数
        q           : 検索ワード
        scroll      : 検索結果の読み取りの量
        
        リターン(辞書内包のリスト型)
        """
        
        
        # serchboxの取得とクエリ送信送信
        self.browser.get("https://twitter.com/search?f=tweets&vertical=news&q="+ q + "&src=typd")
        time.sleep(self.span)
        
        # 指定された回数スクロール
        for i in range(scroll):
            try:
                actions = ActionChains(self.browser)
                actions.send_keys(Keys.END)
                actions.perform()
                time.sleep(self.span)
            except TimeoutException:
                self.logger.info('ti')
                break
        # ツイートストリームの取得
        
        tweet_list = self.browser.find_element_by_css_selector('#stream-items-id')
        tweet_cards = tweet_list.find_elements_by_css_selector('li.js-stream-item.stream-item.stream-item[data-item-type="tweet"]')
        
        tweet_info_dict_list = []
        for i,tweet_card in enumerate(tweet_cards):
            try:
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
                
                tweet_info_dict["tweet_id"] = tweet_id
                tweet_info_dict["username"] = username
                tweet_info_dict["tweet_time"] = tweet_time
                tweet_info_dict["user_id"] = user_id
                tweet_info_dict["conversation_id"] = conversation_id
                tweet_info_dict["retweet"] = action_retweet.split('\n')[-1]
                tweet_info_dict["reply"] = action_reply.split('\n')[-1]
                tweet_info_dict["favorite"] = action_favorite.split('\n')[-1]
                tweet_info_dict["tweet_text"] = text
                yield tweet_info_dict
                #tweet_info_dict_list.append(tweet_info_dict)
            except Exception as e:
                print('[Error]',e)
                self.logger.error(e)
        #return tweet_info_dict_list
    def get_reply_by_original_tweet_id(self,username,tweet_id,scroll=100):
        self.browser.get('https://twitter.com/'+username+'/status/'+tweet_id)
        # スクロール
        for i in range(50):
            try:
                # 返信を更に表示が見つかればクリック
                more_button = browser.find_element_by_css_selector('button.ThreadedConversation-showMoreThreadsButton.u-textUserColor')
                more_button.click()
                print('button click...')
            except:
                pass
            actions = ActionChains(browser)
            actions.send_keys(Keys.END)
            actions.perform()
            time.sleep(self.span)
        # 返信を更に表示をできる限りクリック
        replies = browser.find_element_by_css_selector('div.replies-to.permalink-inner.permalink-replies')
        more_reply_link_list = replies.find_elements_by_css_selector('a.ThreadedConversation-moreRepliesLink')
        for more_reply_link in more_reply_link_list:
            more_reply_link.click()
            
        reply_list = replies.find_elements_by_css_selector('li.ThreadedConversation--loneTweet,div.ThreadedConversation-tweet')
        reply_info_dict_list = []
        for reply in reply_list:
            reply_info_dict = dict()
            content = reply.find_element_by_css_selector('div.tweet.js-stream-tweet.js-actionable-tweet.dismissible-content')
            tweet_id = content.get_attribute("data-tweet-id")
            text = content.find_element_by_css_selector('p.TweetTextSize.js-tweet-text.tweet-text')
            username = content.find_element_by_css_selector('span.username.u-dir.u-textTruncate')
            print(username.text)
            reply_info_dict["tweet_id"] = tweet_id
            reply_info_dict["text"] = text.text
            reply_info_dict["username"] = username.text
            reply_info_dict_list.append(reply_info_dict)
        return reply_info_dict_list
    
    def get_self_uid(self,email,password):
        #自分のuidを返す
        self.login(email=email,password=password)
        time.sleep(self.span)
        profile_icon = self.browser.find_element_by_xpath('//*[@id="user-dropdown-toggle"]')
        profile_icon.click()
        time.sleep(self.span)
        profile_link = self.browser.find_element_by_xpath('//*[@id="user-dropdown"]/div/ul/li[3]/a')
        profile_link.click()
        time.sleep(self.span)
        current_url=self.browser.current_url
        print(current_url)
        uid = str(current_url).split('/')[-1]
        return uid
    def get_following_list(self):
        # フォロー中のユーザを取得しlistで返す
        self.browser.get('https://twitter.com/')
        time.sleep(self.span)
        #「フォロー」クリック
        link_follow = self.browser.find_element_by_xpath('//*[@id="page-container"]/div[1]/div[1]/div/div[3]/ul/li[2]/a/span[2]')
        link_follow.click()
        # javascriptを実行してページの
        # 最下部へ移動
        for i in range(1000):
            actions = ActionChains(self.browser)
            actions.send_keys(Keys.END)
            actions.perform()
            time.sleep(self.span)
        friend_list_box = browser.find_element_by_xpath('//*[@id="page-container"]/div[4]/div/div/div[2]/div/div[2]/div[2]')
        profile_link_list = friend_list_box.find_elements_by_class_name("u-linkComplex-target")
        friend_id_list = []
        for count,profile_link in enumerate(profile_link_list):
            friend_id_list[count] = profile_link.text
        return friend_id_list
    def get_all_tweet_from_uid(self,uid=1,scroll_repetition=1000):
        #uidからそのユーザのすべてのツイートを取得する
        #uid:ユーザid
        #scroll_repetition:ユーザのホームからスクロールする回数
        self.browser.get('https://twitter.com/' + uid)
        time.sleep(self.span)
        #actionを実行してページの最下部へ移動
        for i in range(scroll_repetition):
            actions = ActionChains(self.browser)
            actions.send_keys(Keys.END)
            actions.perform()
        tweet_stream = self.browser.find_element_by_xpath('//div[@data-test-selector="ProfileTimeline"]')
        tweet_list = tweet_stream.find_elements_by_css_selector('.tweet.original-tweet')
        #ツイート情報を入れるlist
        tweet_info_list = []
        
        for tweet in tweet_list:
            tweet_data_item_id = tweet.get_attribute("data-tweet-id")
            tweet_uid_name=tweet.get_attribute("data-screen-name")
            tweet_info = dict()
            tweet_info["main_tweet_id"]=tweet_data_item_id
            tweet_info["uid"] = tweet_uid_name
            tweet_info_list.append(tweet_info)
        return tweet_info_list
    