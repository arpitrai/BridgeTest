from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait, Select
import unittest, time, re

from django.test import LiveServerTestCase

class SeleniumTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        #self.base_url = 'http://localhost:8000'

    def test_a_user_login(self):
        driver = self.driver
        driver.get(self.live_server_url + '/')
        driver.maximize_window()
        driver.find_element_by_link_text('Don\'t have an account? Create account').click()
        driver.find_element_by_id('id_firstname').clear()
        driver.find_element_by_id('id_firstname').send_keys('Arpit Rai')
        driver.find_element_by_id('id_username').clear()
        driver.find_element_by_id('id_username').send_keys('arpitrai@gmail.com')
        driver.find_element_by_id('id_password1').clear()
        driver.find_element_by_id('id_password1').send_keys('arpitrai')
        driver.find_element_by_id('id_password2').clear()
        driver.find_element_by_id('id_password2').send_keys('arpitrai')
        driver.find_element_by_id('save').click()
        self.assertEqual('Home',driver.find_element_by_link_text('Home').text)
        print 'Here'
        driver.find_element_by_link_text('Logout').click()

    def tearDown(self):
        self.driver.quit()
        pass

if __name__ == '__main__':
    unittest.main()
