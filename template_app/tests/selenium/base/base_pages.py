''' module for classes that wrap a single browser page '''
# pylint: disable=E1101
from selenium.webdriver.support.wait import WebDriverWait
from template_app.tests.selenium.base.base_selenium import BaseSeleniumObject,\
    ElementCountEqualWait
from template_app.tests.selenium.base.base_elements import (LoginElement, BaseTextElement,
                                                            NewCigarshopWidget, ExistingCigarshopWidget)
from django_template import settings


class BasePage(BaseSeleniumObject):
    ''' the base page. knows the url and the elements it should wait for on loading. '''

    def __init__(self, driver, full_url):
        super(BasePage, self).__init__(driver)
        self.full_url = full_url
        self.initial_elements = []

    def navigate(self):
        ''' go to a page '''
        self.driver.get(self.full_url)

    def load(self):
        ''' wait for initial elements to show up and load them, fail if any don't become visible '''
        for element in self.initial_elements:
            element.wait_fill()

        for element in self.initial_elements:
            if not element.is_shown():
                raise ValueError("Page %s expected element %s to be visible after loading, but it was not",
                                 self.full_url, element.the_path)

    def navigate_and_load(self):
        ''' navigate to a page and load initial elements '''
        self.navigate()
        self.load()


class WelcomePage(BasePage):
    ''' the welcome page '''

    def __init__(self, driver):
        super(WelcomePage, self).__init__(driver, 'http://127.0.0.1/welcome/')
        self.login_element = LoginElement(self.driver)
        self.login_disclaimer = BaseTextElement(self.driver, "//div/div[contains(text(), 'You must login')]")
        self.initial_elements += [self.login_element, self.login_disclaimer]
        self.new_cigarshop_widget = NewCigarshopWidget(self.driver)
        self.all_shops_path = "//div[contains(@data-ng-repeat, '(id, curshop) in shops') and *[@shop = 'curshop']]"

    def login_good(self, username, password):
        ''' succesfully login and fill out widgets that become visible afterwards '''
        self.login_element.login_good(username, password)
        self.new_cigarshop_widget.fill()

    def get_num_shops(self):
        ''' get the number of existing shops '''
        return len(self.driver.find_elements_by_xpath(self.all_shops_path))

    def get_existing_shop_obj(self, the_name):
        ''' get the object that represents the shop with the provided name '''
        all_shop_elements = self.driver.find_elements_by_xpath(self.all_shops_path)
        for idx in range(len(all_shop_elements)):
            the_path = "%s[%s]" % (self.all_shops_path, idx + 1)
            existing_cigarshop = ExistingCigarshopWidget(self.driver, the_path).fill()
            if existing_cigarshop.get_name() == the_name:
                return existing_cigarshop
        return None

    def create_shop(self, name, the_lat, the_long):
        ''' create a new cigarshop '''
        self.new_cigarshop_widget.create_cigar_shop(name, the_lat, the_long)

    def update_save(self, old_name, new_name, new_lat, new_long):
        ''' update shop and save '''
        self.get_existing_shop_obj(old_name).update_save(new_name, new_lat, new_long)

    def update_cancel(self, old_name, new_name, new_lat, new_long):
        ''' update shop and cancel '''
        self.get_existing_shop_obj(old_name).update_cancel(new_name, new_lat, new_long)

    def delete_shop(self, name):
        ''' delete shop by name and wait for total shops to go down by one '''
        cur_shop_count = self.get_num_shops()
        self.get_existing_shop_obj(name).delete()
        the_wait = ElementCountEqualWait(self.all_shops_path, cur_shop_count - 1)
        WebDriverWait(self.driver, settings.SELENIUM_TIMEOUT_SECONDS).until(the_wait)
