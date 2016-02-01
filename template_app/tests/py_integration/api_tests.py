''' module for request level tastypie api tests '''
# pylint: disable=E1101,  W0212
import json
from django.test.testcases import TestCase
from template_app.models import CigarShop, FaveShops


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

    def test_crud_unauthorized(self):
        '''
            verify that other users attempts to alter a users cigar shops are rejected
        '''
        self.assertEquals(CigarShop.objects.filter(owner__pk=1).count(), 2)
        self.client.login(username='another_test_user', password='testing123')
        cigar_shop_obj = {'name': 'brand new cigar shop',
                          'owner': '/api/v1/auth/user/1/',
                          "location": {"coordinates": [-77.0, 39.0], "type": "Point"}}
        response = self.client.post('/api/v1/cigarshop/',
                                    json.dumps(cigar_shop_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 401)

        response = self.client.get('/api/v1/cigarshop/1/')
        self.assertEquals(response.status_code, 401)

        cigar_shop_obj['name'] = 'the name has been changed'
        # put to update, must include entire obj as all fields get updated
        response = self.client.put('/api/v1/cigarshop/1/',
                                   json.dumps(cigar_shop_obj),
                                   content_type='application/json')
        self.assertEquals(response.status_code, 401)

        response = self.client.patch('/api/v1/cigarshop/1/',
                                     json.dumps({'name': 'no location no problem'}),
                                     content_type='application/json')
        self.assertEquals(response.status_code, 401)

        response = self.client.delete('/api/v1/cigarshop/1/')
        self.assertEquals(response.status_code, 401)

    def test_lat_long_filter(self):
        ''' make sure requests that filter by lat, long and distance work '''
        self.client.login(username='test_user', password='testing123')
        # request that filters narrows results down
        response = self.client.get('/api/v1/cigarshop/?long=-77.0&lat=39.0&distance=0.01')
        self.assertEquals(response.status_code, 200)
        json_obj = json.loads(response.content)
        self.assertEquals(1, len(json_obj['objects']))

        # request the does not gets all results. all 3 params must be present to filter.
        response = self.client.get('/api/v1/cigarshop/?&lat=39.0&distance=0.01')
        self.assertEquals(response.status_code, 200)
        json_obj = json.loads(response.content)
        self.assertEquals(2, len(json_obj['objects']))


class FaveShopsResourceTests(TestCase):
    ''' integration-ish tests for FaveShopsResource '''
    fixtures = ['users_groups_perms.json', 'cigarshops_favs.json']

    def test_crud_success(self):
        '''
            make sure authenticated user able to perform fave shops crud operations
            on fave shops he has access to.
        '''
        self.assertEquals(FaveShops.objects.filter(owner__pk=1).count(), 1)
        fave_shop_obj = {'name': 'another faves list',
                         'owner': '/api/v1/auth/user/1/',
                         'cigar_shops': []}
        self.client.login(username='test_user', password='testing123')
        # post to create a new fave shops list
        response = self.client.post('/api/v1/faveshops/',
                                    json.dumps(fave_shop_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 201)
        self.assertEquals(FaveShops.objects.filter(owner__pk=1).count(), 2)
        new_obj_uri = response._headers['location'][1]

        # get the newly created cigarshop
        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 200)
        retrieved_new_obj = json.loads(response.content)
        self.assertEquals(retrieved_new_obj['name'], fave_shop_obj['name'])

        fave_shop_obj['cigar_shops'].append('/api/v1/cigarshop/1/')
        # put to update, must include entire obj as all fields get updated
        response = self.client.put(new_obj_uri,
                                   json.dumps(fave_shop_obj),
                                   content_type='application/json')
        self.assertEquals(response.status_code, 204)

        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 200)
        retrieved_new_obj = json.loads(response.content)
        self.assertIn('/api/v1/cigarshop/1/', retrieved_new_obj['cigar_shops'])

        # patch to only update a single field
        response = self.client.patch(new_obj_uri,
                                     json.dumps({'cigar_shops': ['/api/v1/cigarshop/2/']}),
                                     content_type='application/json')
        self.assertEquals(response.status_code, 202)

        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 200)
        retrieved_new_obj = json.loads(response.content)
        self.assertIn('/api/v1/cigarshop/2/', retrieved_new_obj['cigar_shops'])

        # delete to get rid of the object
        response = self.client.delete(new_obj_uri)
        self.assertEquals(response.status_code, 204)
        response = self.client.get(new_obj_uri)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(FaveShops.objects.filter(owner__pk=1).count(), 1)

    def test_unowned_relation(self):
        '''
            make sure that the api does not permit user to get a fave_shops
            containing a cigar shop he doesn't own.
        '''
        self.client.login(username='another_test_user', password='testing123')
        fave_shop_obj = {'name': 'another faves list',
                         'owner': '/api/v1/auth/user/2/',
                         'cigar_shops': ['/api/v1/cigarshop/1/']}
        response = self.client.post('/api/v1/faveshops/',
                                    json.dumps(fave_shop_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 401)

        fave_shop_obj['cigar_shops'] = []
        response = self.client.post('/api/v1/faveshops/',
                                    json.dumps(fave_shop_obj),
                                    content_type='application/json')
        self.assertEquals(response.status_code, 201)
        new_obj_uri = response._headers['location'][1]

        fave_shop_obj['cigar_shops'].append('/api/v1/cigarshop/1/')
        response = self.client.put(new_obj_uri,
                                   json.dumps(fave_shop_obj),
                                   content_type='application/json')
        self.assertEquals(response.status_code, 401)

        response = self.client.patch(new_obj_uri,
                                     json.dumps({'cigar_shops': ['/api/v1/cigarshop/2/']}),
                                     content_type='application/json')
        self.assertEquals(response.status_code, 401)
