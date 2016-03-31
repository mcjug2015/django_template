''' module for wrappers around page elements '''
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from template_app.tests.selenium.base.base_selenium import BaseSeleniumObject
from django_template import settings


class BaseElement(BaseSeleniumObject):
    ''' the base element, knows its xpath, can load the corresponding webelement. '''

    def __init__(self, driver, the_path):
        super(BaseElement, self).__init__(driver)
        self.the_path = the_path
        self.the_element = None

    def is_shown(self):
        ''' pass own path to superclass method '''
        return super(BaseElement, self).is_visible(self.the_path)

    def fill(self):
        ''' load the web_element this class wraps '''
        self.the_element = self.driver.find_element_by_xpath(self.the_path)

    def wait(self):
        ''' wait for the elements xpath to be displayed on the page '''
        the_wait = EC.visibility_of_element_located((By.XPATH, self.the_path))
        WebDriverWait(self.driver, settings.SELENIUM_TIMEOUT_SECONDS).until(the_wait)

    def wait_fill(self):
        ''' wait for element xpath to become displayed and fill it '''
        self.wait()
        self.fill()
