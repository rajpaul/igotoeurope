from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
from django.test import LiveServerTestCase


class UserSignupTest(LiveServerTestCase):
    
    def setUp(self):  #2
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):  #3
        self.browser.quit()


    def test_user_can_sign_up(self):
    	self.browser.get(self.live_server_url)

