''' base test classes that actual selenium classes can override and make use of '''
# pylint: disable=E1101,E0611
import os
import string
import random
import requests
from django.test.testcases import TestCase
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from django_template import settings


class BaseSeleniumTest(TestCase):
    ''' basic selenium test that sets up a driver '''

    def setUp(self):
        ''' set up test '''
        os.environ["DISPLAY"] = ":99"
        ffx_bin = FirefoxBinary("/usr/bin/firefox")
        self.driver = webdriver.Firefox(firefox_binary=ffx_bin)

    def tearDown(self):
        ''' tear down test '''
        self.driver.close()

    @classmethod
    def get_full_url(cls, path_appendix):
        ''' get the full url by combining selenium base url setting value with appendix '''
        if not path_appendix.startswith('/'):
            path_appendix = '/%s' % path_appendix
        return settings.SELENIUM_BASE_URL + path_appendix


class BaseUserSeleniumTest(BaseSeleniumTest):
    ''' base test case that sets up a valid user of the site '''

    @classmethod
    def id_generator(cls, size=6, chars=string.ascii_uppercase + string.digits):
        ''' generate a username appendix '''
        return ''.join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_user(cls, username):
        ''' ask the server to create a user, return dict with username, password '''
        the_url = cls.get_full_url('/selenium/create_user/?username=%s' % username)
        response = requests.get(the_url)
        return response.json()

    @classmethod
    def remove_user(cls, username):
        ''' ask the server to remove user by username '''
        requests.get(cls.get_full_url('/selenium/remove_user/?username=%s' % username))

    def setUp(self):
        ''' set up the test '''
        super(BaseUserSeleniumTest, self).setUp()
        self.username = 'selenium_user_%s' % self.id_generator()
        self.the_user = self.create_user(self.username)

    def tearDown(self):
        ''' tear down the test '''
        super(BaseUserSeleniumTest, self).tearDown()
        self.remove_user(self.username)
