''' module for wrappers around page elements '''
# pylint: disable=E1101,E0611
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
        return self

    def wait(self):
        ''' wait for the elements xpath to be displayed on the page '''
        the_wait = EC.visibility_of_element_located((By.XPATH, self.the_path))
        WebDriverWait(self.driver, settings.SELENIUM_TIMEOUT_SECONDS).until(the_wait)

    def wait_fill(self):
        ''' wait for element xpath to become displayed and fill it '''
        self.wait()
        self.fill()
        return self

    def get_child_element(self, path_appendix, the_type="base"):
        ''' get an element that is the child of this element '''
        child_path = self.get_child_path(path_appendix)
        if the_type == 'base':
            return BaseElement(self.driver, child_path)
        elif the_type == 'text':
            return BaseTextElement(self.driver, child_path)
        elif the_type == 'click':
            return BaseClickableElement(self.driver, child_path)
        else:
            raise ValueError("%s is not a valid child element type", the_type)

    def get_child_path(self, path_appendix):
        ''' get the path to the child element based on own path and an appendix '''
        return "%s//%s" % (self.the_path, path_appendix)


class BaseTextElement(BaseElement):
    ''' An element that can contain text and get text sent to it '''

    def get_text(self):
        ''' get the text, stripped for convinience '''
        return self.the_element.text.strip()

    def set_text(self, the_text):
        ''' set the elements text '''
        self.the_element.send_keys(the_text)


class BaseClickableElement(BaseElement):
    ''' An element that can be clicked on '''

    def click(self):
        ''' click on the element '''
        self.the_element.click()

    def click_and_wait(self, the_wait, timeout=settings.SELENIUM_TIMEOUT_SECONDS):
        ''' click on the element and wait for something to happen '''
        self.click()
        WebDriverWait(self.driver, timeout=timeout).until(the_wait)


class LoginElement(BaseElement):
    ''' element wrapping the login fields '''

    def __init__(self, driver):
        super(LoginElement, self).__init__(driver, "//div[button[contains(text(), 'login')]]")
        self.username_text_path = "input[@type='text']"
        self.password_text_path = "input[@type='password']"
        self.login_button_path = "button[contains(text(), 'login')]"
        self.expected_post_good_login_path = "//div/div[contains(text(), 'Welcome to the app')]"
        self.the_wait = EC.visibility_of_element_located((By.XPATH, self.expected_post_good_login_path))

    def login_good(self, username, password):
        ''' fill out login form and wait for welcome to the app text to appear '''
        self.get_child_element(self.username_text_path, "text").fill().set_text(username)
        self.get_child_element(self.password_text_path, "text").fill().set_text(password)
        self.get_child_element(self.login_button_path, "click").fill().click_and_wait(self.the_wait)


class NewCigarshopWidget(BaseElement):
    ''' a widget for creating new cigarshops '''

    def __init__(self, driver):
        super(NewCigarshopWidget, self).__init__(driver, "//div[button[text()='Create']]")
        self.name_xpath = "div/input[@data-ng-model = 'shop.name']"
        self.lat_xpath = "div/div[contains(text(), 'Lat:')]/input[@data-ng-model = 'shop.location.lat']"
        self.long_xpath = "div/div[contains(text(), 'Long:')]/input[@data-ng-model = 'shop.location.long']"
        self.create_button_xpath = "button[text()='Create']"

    def create_cigar_shop(self, name, the_lat, the_long):
        ''' create a new cigar shop with params provided. '''
        self.get_child_element(self.name_xpath, "text").fill().set_text(name)
        self.get_child_element(self.lat_xpath, "text").fill().set_text(the_lat)
        self.get_child_element(self.long_xpath, "text").fill().set_text(the_long)

        new_shop_xpath = "//div[span[contains(text(), 'Here are your existing')]]/"
        new_shop_xpath += "div[contains(@data-ng-repeat, 'in shops')]//div/div[contains(text(), '%s')]" % name
        the_wait = EC.visibility_of_element_located((By.XPATH, new_shop_xpath))
        self.get_child_element(self.create_button_xpath,
                               "click").fill().click_and_wait(the_wait)
