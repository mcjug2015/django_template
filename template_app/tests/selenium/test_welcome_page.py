''' first selenium test, mostly to make sure everything is setup right '''
from template_app.tests.selenium.base.base_pages import WelcomePage
from template_app.tests.selenium.base.base_tests import BaseUserSeleniumTest


class WelcomePageTest(BaseUserSeleniumTest):
    ''' Login, go to welcome page, make sure cigarshop manipulation works '''

    def verify_shop(self, welcome_page, name, the_lat, the_long):
        ''' verify that values in the shop are equal to the ones provided '''
        the_shop = welcome_page.get_existing_shop_obj(name)
        self.assertEquals(the_shop.get_name(), name)
        self.assertEquals(the_shop.get_lat(), the_lat)
        self.assertEquals(the_shop.get_long(), the_long)

    def verify_update_cancel_delete(self, welcome_page, values):
        '''
            verify shop info, update cigarshop with new info, verify it,
            do update and cancel, delete cigarshop.
        '''
        self.verify_shop(welcome_page, values['initial_name'], values['initial_lat'], values['initial_long'])
        welcome_page.update_save(values['initial_name'],
                                 values['new_name'],
                                 values['new_lat'],
                                 values['new_long'])
        self.verify_shop(welcome_page, values['new_name'], values['new_lat'], values['new_long'])
        welcome_page.update_cancel(values['new_name'], values['cancel_name'],
                                   values['cancel_lat'], values['cancel_long'])
        self.verify_shop(welcome_page, values['new_name'], values['new_lat'], values['new_long'])
        welcome_page.delete_shop(values['new_name'])

    def test_fresh_cigarshops(self):
        ''' make sure that newly created cigarshops can be updated and deleted '''
        self.create_cigarshop("Existing Shop", "35.555551", "-75.555551")
        welcome_page = WelcomePage(self.driver)
        welcome_page.navigate_and_load()
        self.assertEquals(welcome_page.login_disclaimer.get_text(),
                          "You must login to use this site")
        welcome_page.login_good(self.the_user['username'],
                                self.the_user['password'])
        self.assertEquals(1, welcome_page.get_num_shops())
        welcome_page.create_shop("Selenium created shop",
                                 "39.999111", "-77.333444")
        self.assertEquals(2, welcome_page.get_num_shops())
        welcome_page.create_shop("Another Selenium created shop",
                                 "38.888888", "-79.111222")
        self.assertEquals(3, welcome_page.get_num_shops())

        self.verify_update_cancel_delete(welcome_page, {'initial_name': 'Selenium created shop',
                                                        'initial_lat': '39.999111',
                                                        'initial_long': '-77.333444',
                                                        'new_name': 'OMNOMNOM',
                                                        'new_lat': '36.999111',
                                                        'new_long': '-79.333444',
                                                        'cancel_name': 'a',
                                                        'cancel_lat': 'b',
                                                        'cancel_long': 'c'})
        self.assertEquals(2, welcome_page.get_num_shops())
        self.verify_update_cancel_delete(welcome_page, {'initial_name': 'Another Selenium created shop',
                                                        'initial_lat': '38.888888',
                                                        'initial_long': '-79.111222',
                                                        'new_name': 'ZZZZZZZZ',
                                                        'new_lat': '31.999999',
                                                        'new_long': '-71.999999',
                                                        'cancel_name': 'x',
                                                        'cancel_lat': 'y',
                                                        'cancel_long': 'z'})
        self.assertEquals(1, welcome_page.get_num_shops())
        self.verify_update_cancel_delete(welcome_page, {'initial_name': 'Existing Shop',
                                                        'initial_lat': '35.555551',
                                                        'initial_long': '-75.555551',
                                                        'new_name': 'Last shop standing',
                                                        'new_lat': '35.555552',
                                                        'new_long': '-75.555552',
                                                        'cancel_name': 'ax',
                                                        'cancel_lat': 'by',
                                                        'cancel_long': 'cz'})
        self.assertEquals(0, welcome_page.get_num_shops())
