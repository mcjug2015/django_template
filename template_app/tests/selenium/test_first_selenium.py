''' first selenium test, mostly to make sure everything is setup right '''
from template_app.tests.selenium.base.base_pages import WelcomePage
from template_app.tests.selenium.base.base_tests import BaseUserSeleniumTest


class FirstTest(BaseUserSeleniumTest):
    ''' Class for making sure selenium works ok '''

    def test_first(self):
        ''' verify that selenium tests can happen '''
        welcome_page = WelcomePage(self.driver)
        welcome_page.navigate_and_load()
        self.assertEquals(welcome_page.login_disclaimer.get_text(),
                          "You must login to use this site")
        welcome_page.login_element.login_good(self.the_user['username'],
                                              self.the_user['password'])
