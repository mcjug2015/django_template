''' first selenium test, mostly to make sure everything is setup right '''
import os
from django.test.testcases import TestCase
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        self.driver.get("http://127.0.0.1/welcome/")
        the_wait = EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'login')]"))
        WebDriverWait(self.driver, timeout=3).until(the_wait)
