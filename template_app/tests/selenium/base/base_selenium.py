''' module for base selenium objects '''


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
