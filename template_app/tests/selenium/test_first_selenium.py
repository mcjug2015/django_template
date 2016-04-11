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
        welcome_page.login_good(self.the_user['username'],
                                self.the_user['password'])
        self.assertEquals(0, welcome_page.get_num_shops())
        welcome_page.create_shop("Selenium created shop",
                                 "39.999111", "-77.333444")
        self.assertEquals(1, welcome_page.get_num_shops())
        welcome_page.create_shop("Another Selenium created shop",
                                 "38.888888", "-79.111222")
        self.assertEquals(2, welcome_page.get_num_shops())
        shop1 = welcome_page.get_existing_shop_obj("Selenium created shop")
        shop2 = welcome_page.get_existing_shop_obj("Another Selenium created shop")
        self.assertEquals(shop1.get_name(), "Selenium created shop")
        self.assertEquals(shop1.get_lat(), "39.999111")
        self.assertEquals(shop1.get_long(), "-77.333444")
        self.assertEquals(shop2.get_name(), "Another Selenium created shop")
        self.assertEquals(shop2.get_lat(), "38.888888")
        self.assertEquals(shop2.get_long(), "-79.111222")

        welcome_page.update_save("Selenium created shop", "OMNOMNOM", "36.999111", "-79.333444")
        welcome_page.update_cancel("Another Selenium created shop", "ZZZZZZZ",
                                   "36.555000", "-79.8675309")
        self.assertIsNone(welcome_page.get_existing_shop_obj("Selenium created shop"))
        shop1 = welcome_page.get_existing_shop_obj("OMNOMNOM")
        shop2 = welcome_page.get_existing_shop_obj("Another Selenium created shop")
        self.assertEquals(shop1.get_name(), "OMNOMNOM")
        self.assertEquals(shop1.get_lat(), "36.999111")
        self.assertEquals(shop1.get_long(), "-79.333444")
        self.assertEquals(shop2.get_name(), "Another Selenium created shop")
        self.assertEquals(shop2.get_lat(), "38.888888")
        self.assertEquals(shop2.get_long(), "-79.111222")
        self.assertEquals(2, welcome_page.get_num_shops())

        welcome_page.delete_shop("OMNOMNOM")
        self.assertEquals(1, welcome_page.get_num_shops())
        welcome_page.delete_shop("Another Selenium created shop")
        self.assertEquals(0, welcome_page.get_num_shops())
