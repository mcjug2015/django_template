''' module for request level tastypie api tests '''
# pylint: disable=E1101
import json
from django.test.testcases import TestCase


class UserResourceTests(TestCase):
    '''
        test class that sends requests to the UserResource endpoint,
        makes sure users can only view other users they have right to view.
    '''
    fixtures = ['users_groups_perms.json']

    def test_get_success(self):
        ''' make sure logged in user can only get list/detail with himself '''
        self.client.login(username='test_user', password='testing123')
        response = self.client.get('/api/v1/auth/user/')
        self.assertEquals(response.status_code, 200)
        json_obj = json.loads(response.content)
        self.assertEquals(len(json_obj['objects']), 1)
        self.assertEquals(json_obj['objects'][0]['username'], 'test_user')

        response = self.client.get('/api/v1/auth/user/1/')
        self.assertEquals(response.status_code, 200)
        json_obj = json.loads(response.content)
        self.assertEquals(json_obj['username'], 'test_user')

    def test_get_unauthorized(self):
        ''' make sure we fail to get another user's object '''
        self.client.login(username='test_user', password='testing123')
        response = self.client.get('/api/v1/auth/user/?username=another_test_user')
        self.assertEquals(response.status_code, 200)
        json_obj = json.loads(response.content)
        self.assertEquals(len(json_obj['objects']), 0)

        response = self.client.get('/api/v1/auth/user/2/')
        self.assertEquals(response.status_code, 401)
