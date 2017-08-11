from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

class Twitter:
    def __init__(self, username=None, password=None):
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(2560, 1000)
        self.username = username
        self.password = password
        self.base_url = "https://twitter.com"
        
    def login(self):
        start = time.time()
        login_url = "https://twitter.com/login"
        self.browser.get(login_url)
        username_field = self.browser.find_element_by_class_name('js-username-field')
        password_field = self.browser.find_element_by_class_name('js-password-field')
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.ENTER)
        self.browser.maximize_window()
        print "LOGIN PROCESS: {} seconds elapsed".format(time.time() - start)
        time.sleep(1)

    def get_followers(self, user):
        start = time.time()
        user_url = "{}/{}/{}".format(self.base_url, user, "followers")
        self.browser.get(user_url)
        time.sleep(.2)
        body = self.browser.find_element_by_tag_name('body')
        num_followers = int((self.browser.find_elements_by_class_name('ProfileNav-value')[2].text).replace(',', ''))
        print "{} has {} Followers".format(user, num_followers)
        for i in range(num_followers/3):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.03)
            following = map(lambda x: x.get_attribute('data-screen-name'), self.browser.find_elements_by_class_name('ProfileCard'))
            if len(following) == num_followers:
                break
        followers = map(lambda x: x.get_attribute('data-screen-name'), self.browser.find_elements_by_class_name('ProfileCard'))
        print "RETRIEVED {} FOLLOWERS {}: {} seconds elapsed".format(user, len(followers), time.time() - start)
        
        return followers

    def get_following(self, user):
        start = time.time()
        user_url = "{}/{}/{}".format(self.base_url, user, "following")
        self.browser.get(user_url)
        body = self.browser.find_element_by_tag_name('body')
        num_followers = int((self.browser.find_elements_by_class_name('ProfileNav-value')[1].text).replace(',', ''))
        print "{} has {} Followers".format(user, num_followers)
        for i in range(num_followers/3):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(.03)
        followers = map(lambda x: x.get_attribute('data-screen-name'), self.browser.find_elements_by_class_name('ProfileCard'))
        print "RETRIEVED {} FOLLOWERS {}: {} seconds elapsed".format(user, len(followers), time.time() - start)
        
        return followers



    def get_followers_you_follow(self, user):
        start = time.time()
        user_url = "{}/{}/{}".format(self.base_url, user, "followers_you_follow")
        self.browser.get(user_url)
        source = self.browser.page_source
        start = source.index("you know")
        if start == -1:
            raise ValueError('No such instance')
            return []
        unionFollowers = source[start - 15: start]
        if 'people' not in unionFollowers:
            unionFollowers = int(unionFollowers[unionFollowers.index(">")+1:unionFollowers.index(" ")])
            child_body = self.browser.find_element_by_tag_name('body')
            for _ in range(unionFollowers):
                child_body.send_keys(Keys.PAGE_DOWN)
                time.sleep(.05)
            child_followers = map(lambda x: x.get_attribute('data-screen-name'), self.browser.find_elements_by_class_name('ProfileCard'))
            print "Shared Followers {}: {}".format(user, unionFollowers)
            for i in range(unionFollowers/3):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(.03)
            followers = map(lambda x: x.get_attribute('data-screen-name'), self.browser.find_elements_by_class_name('ProfileCard'))
            print "RETRIEVED {} FOLLOWERS {}: {} seconds elapsed".format(user, len(followers), time.time() - start)
            return followers
        return []

    def quit(self):
        self.browser.quit()
'''
