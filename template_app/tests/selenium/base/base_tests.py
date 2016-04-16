''' base test classes that actual selenium classes can override and make use of '''
# pylint: disable=E1101,E0611
import os
import string
import random
import json
import requests
from django.test.testcases import TestCase
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium import webdriver
from django_template import settings


class BaseSeleniumTest(TestCase):
    ''' basic selenium test that sets up a driver '''

    def setUp(self):
        ''' set up test '''
        os.environ["DISPLAY"] = ":99"
        ffx_bin = FirefoxBinary("/usr/bin/firefox")
        ffx_profile = FirefoxProfile()
        ffx_profile.accept_untrusted_certs = True
        self.driver = webdriver.Firefox(firefox_binary=ffx_bin,
                                        firefox_profile=ffx_profile)

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
        response = requests.get(the_url, verify=False)
        response.raise_for_status()
        return response.json()

    @classmethod
    def remove_user(cls, username):
        ''' ask the server to remove user by username '''
        response = requests.get(cls.get_full_url('/selenium/remove_user/?username=%s' % username),
                                verify=False)
        response.raise_for_status()

    def fill_csrf_cookies(self):
        ''' get a csrf token for posts and such '''
        if not self.csrf_cookies:
            client = requests.session()
            response = client.get(self.get_full_url('/welcome/'), verify=False)
            response.raise_for_status()
            self.csrf_cookies = dict(client.cookies)

    def create_cigarshop(self, name, the_lat, the_long):
        ''' create a cigarshop owned by the user this test created while setting up '''
        self.fill_csrf_cookies()
        json_obj = {'name': name,
                    'lat': the_lat,
                    'long': the_long,
                    'username': self.the_user['username']}
        the_headers = {'Content-type': 'application/json',
                       "X-CSRFToken": self.csrf_cookies['csrftoken'],
                       "REFERER": self.get_full_url("/welcome/"),
                       "HOST": settings.SELENIUM_HOST}
        response = requests.post(self.get_full_url('/selenium/create_shop/'),
                                 data=json.dumps(json_obj),
                                 headers=the_headers,
                                 cookies=self.csrf_cookies,
                                 verify=False)
        response.raise_for_status()

    def setUp(self):
        ''' set up the test '''
        super(BaseUserSeleniumTest, self).setUp()
        self.csrf_cookies = None
        self.username = 'selenium_user_%s' % self.id_generator()
        self.the_user = self.create_user(self.username)

    def tearDown(self):
        ''' tear down the test '''
        super(BaseUserSeleniumTest, self).tearDown()
        self.remove_user(self.username)
