'''
    module for views unit tests.
'''
# pylint: disable=E1101
import json
from django.test.testcases import TestCase
from django.contrib.auth.models import User


class LoginAsyncTests(TestCase):
    ''' class for login_async views method '''
    fixtures = ['users_groups_perms.json']

    def test_invalid_login(self):
        ''' make sure we get 403 status code when wrong u/p is provided '''
        json_input = {'username': 'wrong', 'password': 'wrongovich'}
        response = self.client.post('/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status_code'], 403)
        self.assertEquals(resp_obj['status'], 'wrong u/p')

    def test_inactive_user(self):
        ''' verify that we get a 403 when an inactive user tries to login '''
        the_user = User.objects.get(pk=1)
        the_user.is_active = False
        the_user.save()
        json_input = {'username': 'test_user', 'password': 'testing123'}
        response = self.client.post('/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status_code'], 403)
        self.assertEquals(resp_obj['status'], 'inactive user, go away')

    def test_success(self):
        ''' verify that we get a 200 with good creds '''
        json_input = {'username': 'test_user', 'password': 'testing123'}
        response = self.client.post('/login_async/',
                                    content_type='application/json',
                                    data=json.dumps(json_input))
        self.assertEquals(response.status_code, 200)
        resp_obj = json.loads(response.content)
        self.assertEquals(resp_obj['status_code'], 200)
        self.assertEquals(resp_obj['status'], 'good to go')
