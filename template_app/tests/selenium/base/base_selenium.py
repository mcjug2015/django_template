''' module for base selenium objects '''
from selenium.common.exceptions import StaleElementReferenceException


class ElementCountEqualWait(object):
    """
        Wait for element count to be equal to passed in value
    """
    def __init__(self, the_path, expected_count):
        self.the_path = the_path
        self.expected_count = expected_count

    def __call__(self, driver):
        num_elements = 0
        the_elements = driver.find_elements_by_xpath(self.the_path)
        for element in the_elements:
            try:
                if element.is_displayed():
                    num_elements += 1
            except StaleElementReferenceException:
                # noop, happens when element isn't in the dom anymore
                pass
        if num_elements == self.expected_count:
            return True
        return False


class BaseSeleniumObject(object):
    ''' the basic selenium object, supplies low level convinience methods '''

    def __init__(self, driver):
        self.driver = driver

    def is_visible(self, the_path):
        ''' true if at least one element with the specified xpath is visible '''
        all_elements = self.driver.find_elements_by_xpath(the_path)
        for element in all_elements:
            if element.is_displayed():
                return True
        return False
