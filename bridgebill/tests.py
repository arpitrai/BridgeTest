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

    def test_a_user_signup(self):
        driver = self.driver
        driver.get(self.live_server_url + '/')
        driver.maximize_window()
        driver.find_element_by_link_text('Don\'t have an account? Create account').click()
        driver.find_element_by_id('id_firstname').clear()
        driver.find_element_by_id('id_firstname').send_keys('Arpit Rai')
        driver.find_element_by_id('id_username').clear()
        driver.find_element_by_id('id_username').send_keys('arpitrai@browserstack.com')
        driver.find_element_by_id('id_password1').clear()
        driver.find_element_by_id('id_password1').send_keys('arpitrai')
        driver.find_element_by_id('id_password2').clear()
        driver.find_element_by_id('id_password2').send_keys('arpitrai')
        driver.find_element_by_id('save').click()
        self.assertEqual('Home',driver.find_element_by_link_text('Home').text)
        #driver.find_element_by_link_text('Logout').click()

#    def test_b_user_login_and_friend_creation(self):
        #driver = self.driver
        #driver.get(self.live_server_url + '/')
        #driver.maximize_window()
        #driver.find_element_by_link_text('Don\'t have an account? Create account').click()
        #driver.find_element_by_id('id_firstname').clear()
        #driver.find_element_by_id('id_firstname').send_keys('Arpit Rai')
        #driver.find_element_by_id('id_username').clear()
        #driver.find_element_by_id('id_username').send_keys('arpitrai@browserstack.com')
        #driver.find_element_by_id('id_password1').clear()
        #driver.find_element_by_id('id_password1').send_keys('arpitrai')
        #driver.find_element_by_id('id_password2').clear()
        #driver.find_element_by_id('id_password2').send_keys('arpitrai')
        #driver.find_element_by_id('save').click()
        ##driver.find_element_by_id('id_username').clear()
        ##driver.find_element_by_id('id_username').send_keys('arpitrai@browserstack.com')
        ##driver.find_element_by_id('id_password').clear()
        ##driver.find_element_by_id('id_password').send_keys('arpitrai')
        ##driver.find_element_by_id('submit').click()
        ##self.assertEqual('Home',driver.find_element_by_link_text('Home').text)
        #driver.find_element_by_link_text('My Profile').click()
        #driver.find_element_by_link_text('0 Friends').click()
        #driver.find_element_by_class_name('add_friend').click()
        #driver.find_element_by_id('id_name_0').clear()
        #driver.find_element_by_id('id_name_0').send_keys('Arpit Rai @Gmail')
        #driver.find_element_by_id('id_email_0').clear()
        #driver.find_element_by_id('id_email_0').send_keys('arpitrai@gmail.com')
        #driver.find_element_by_class_name('save_friend_2').click()
        #driver.find_element_by_link_text('Logout').click()

    #def test_d_bill_creation(self):
        #driver = self.driver
        #driver.get(self.live_server_url + '/')
        #driver.maximize_window()
        #driver.find_element_by_link_text('Don\'t have an account? Create account').click()
        #driver.find_element_by_id('id_firstname').clear()
        #driver.find_element_by_id('id_firstname').send_keys('Arpit Rai')
        #driver.find_element_by_id('id_username').clear()
        #driver.find_element_by_id('id_username').send_keys('arpitrai@browserstack.com')
        #driver.find_element_by_id('id_password1').clear()
        #driver.find_element_by_id('id_password1').send_keys('arpitrai')
        #driver.find_element_by_id('id_password2').clear()
        #driver.find_element_by_id('id_password2').send_keys('arpitrai')
        #driver.find_element_by_id('save').click()
        #driver.find_element_by_link_text('My Profile').click()
        #driver.find_element_by_link_text('0 Friends').click()
        #driver.find_element_by_class_name('add_friend').click()
        #driver.find_element_by_id('id_name_0').clear()
        #driver.find_element_by_id('id_name_0').send_keys('Arpit Rai @Gmail')
        #driver.find_element_by_id('id_email_0').clear()
        #driver.find_element_by_id('id_email_0').send_keys('arpitrai@gmail.com')
        #driver.find_element_by_class_name('save_friend_2').click()
        #driver.find_element_by_link_text('Record Bill').click()
        #driver.find_element_by_id('record_bill_option_equal').click()
        #driver.find_element_by_name('date').clear()
        #driver.find_element_by_name('date').send_keys('07/07/2012')
        #driver.find_element_by_name('date').send_keys(Keys.ESCAPE)
        #driver.find_element_by_id('id_description').clear()
        #driver.find_element_by_id('id_description').send_keys('Testing Selenium')
        #driver.find_element_by_id('id_amount').clear()
        #driver.find_element_by_id('id_amount').send_keys('200')
        #persons = driver.find_elements_by_name('people')
        #for person in persons:
            #person.click()
        #driver.find_element_by_id('save').click()
        ##assert 'Bill Created Successfully!' in driver.find_element_by_id('home_details_header').text
        #self.assertEqual('Bill Created Successfully!', driver.find_element_by_id('home_details_header').text)
        #driver.find_element_by_link_text('Home').click()
        #driver.find_element_by_link_text('Logout').click()

    #def test_e_bill_payment(self):
        #driver = self.driver
        #driver.get(self.live_server_url + '/')
        #driver.maximize_window()
        #driver.find_element_by_link_text('Don\'t have an account? Create account').click()
        #driver.find_element_by_id('id_firstname').clear()
        #driver.find_element_by_id('id_firstname').send_keys('Arpit Rai')
        #driver.find_element_by_id('id_username').clear()
        #driver.find_element_by_id('id_username').send_keys('arpitrai@browserstack.com')
        #driver.find_element_by_id('id_password1').clear()
        #driver.find_element_by_id('id_password1').send_keys('arpitrai')
        #driver.find_element_by_id('id_password2').clear()
        #driver.find_element_by_id('id_password2').send_keys('arpitrai')
        #driver.find_element_by_id('save').click()
        #driver.find_element_by_link_text('My Profile').click()
        #driver.find_element_by_link_text('0 Friends').click()
        #driver.find_element_by_class_name('add_friend').click()
        #driver.find_element_by_id('id_name_0').clear()
        #driver.find_element_by_id('id_name_0').send_keys('Arpit Rai @Gmail')
        #driver.find_element_by_id('id_email_0').clear()
        #driver.find_element_by_id('id_email_0').send_keys('arpitrai@gmail.com')
        #driver.find_element_by_class_name('save_friend_2').click()
        #driver.find_element_by_link_text('Record Bill').click()
        #driver.find_element_by_id('record_bill_option_equal').click()
        #driver.find_element_by_name('date').clear()
        #driver.find_element_by_name('date').send_keys('07/07/2012')
        #driver.find_element_by_name('date').send_keys(Keys.ESCAPE)
        #driver.find_element_by_id('id_description').clear()
        #driver.find_element_by_id('id_description').send_keys('Testing Selenium')
        #driver.find_element_by_id('id_amount').clear()
        #driver.find_element_by_id('id_amount').send_keys('200')
        #persons = driver.find_elements_by_name('people')
        #for person in persons:
            #person.click()
        #driver.find_element_by_id('save').click()
        #driver.find_element_by_link_text('Settle Payment').click()
        
        ## Start - To select person
        #select = Select(driver.find_element_by_id('id_person'))
        #select.select_by_visible_text('Arpit Rai @Gmail - arpitrai@gmail.com')
        ## End - To select person

        #self.assertEqual('Bills', driver.find_element_by_id('bills').text)
        #bills = driver.find_elements_by_name('billdetail_id')
        #for bill in bills:
            #bill.click()
            #break
        #driver.find_element_by_id('save').click()
        #self.assertEqual('Success! Bills Settled with Arpit Rai @Gmail', driver.find_element_by_class_name('page_header').text)



    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
