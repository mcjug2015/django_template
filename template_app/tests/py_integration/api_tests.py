''' module for request level tastypie api tests '''
# pylint: disable=E1101,  W0212
import json
from django.test.testcases import TestCase
from template_app.models import CigarShop


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


class CigarShopResourceTests(TestCase):
    ''' integration-ish tests for the cigarshop resource '''
    fixtures = ['users_groups_perms.json', 'cigarshops_favs.json']

    def test_crud_success(self):
        ''' test the crud methods '''
        self.assertEquals(CigarShop.objects.filter(owner__pk=1).count(), 2)
        cigar_shop_obj = {'name': 'brand new cigar shop',
                          'owner': '/api/v1/auth/user/1/',
                          "location": {"coordinates": [-77.0, 39.0], "type": "Point"}}
        self.client.login(username='test_user', password='testing123')
        # post to create a new cigarshop
        response = self.client.post('/api/v1/cigarshop/',
                                    json.dumps(cigar_shop_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 201)
        self.assertEquals(CigarShop.objects.filter(owner__pk=1).count(), 3)
        new_obj_uri = response._headers['location'][1]

        # get the newly created cigarshop
        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 200)
        retrieved_new_obj = json.loads(response.content)
        self.assertEquals(retrieved_new_obj['name'], cigar_shop_obj['name'])

        cigar_shop_obj['name'] = 'the name has been changed'
        # put to update, must include entire obj as all fields get updated
        response = self.client.put(new_obj_uri,
                                   json.dumps(cigar_shop_obj),
                                   content_type='application/json')
        self.assertEquals(response.status_code, 204)

        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 200)
        retrieved_new_obj = json.loads(response.content)
        self.assertEquals(retrieved_new_obj['name'], 'the name has been changed')

        # patch to only update a single field
        response = self.client.patch(new_obj_uri,
                                     json.dumps({'name': 'no location no problem'}),
                                     content_type='application/json')
        self.assertEquals(response.status_code, 202)

        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 200)
        retrieved_new_obj = json.loads(response.content)
        self.assertEquals(retrieved_new_obj['name'], 'no location no problem')

        # delete to get rid of the object
        response = self.client.delete(new_obj_uri)
        self.assertEquals(response.status_code, 204)
        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(CigarShop.objects.filter(owner__pk=1).count(), 2)
