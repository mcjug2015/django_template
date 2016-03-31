''' first selenium test, mostly to make sure everything is setup right '''
import os
from django.test.testcases import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from template_app.tests.selenium.base.base_pages import WelcomePage


class FirstTest(TestCase):
    ''' Class for making sure selenium works ok '''

    def setUp(self):
        ''' set up test '''
        os.environ["DISPLAY"] = ":99"
        ffx_bin = FirefoxBinary("/usr/bin/firefox")
        self.driver = webdriver.Firefox(firefox_binary=ffx_bin)

    def tearDown(self):
        ''' tear down test '''
        self.driver.close()

    def test_first(self):
        ''' verify that selenium tests can happen '''
        welcome_page = WelcomePage(self.driver)
        welcome_page.navigate_and_load()
        self.assertEquals(welcome_page.login_disclaimer.the_element.text.strip(),
                          "You must login to use this site")
