''' unit tests for the api auth module '''
from tastypie.exceptions import Unauthorized
from django.contrib.auth.models import User
from django.test.testcases import TestCase
from mockito.mockito import unstub, mock
from template_app.api_auth import UserObjectsAuthorization,\
    OwnerObjectsOnlyAuthorization
from template_app.models import CigarShop


class UserObjectsAuthorizationTests(TestCase):
    ''' test class for UserObjectsAuthorization '''
    fixtures = ['users_groups_perms.json']

    def setUp(self):
        ''' set up the test '''
        self.the_auth = UserObjectsAuthorization()

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_unoauthorized_methods(self):
        ''' make sure unauthorized methods raise the unauthorised exception '''
        self.assertRaises(Unauthorized, self.the_auth.update_detail, None, None)
        self.assertRaises(Unauthorized, self.the_auth.update_list, None, None)
        self.assertRaises(Unauthorized, self.the_auth.create_detail, None, None)
        self.assertRaises(Unauthorized, self.the_auth.create_list, None, None)
        self.assertRaises(Unauthorized, self.the_auth.delete_detail, None, None)
        self.assertRaises(Unauthorized, self.the_auth.delete_list, None, None)

    def test_read_unauthorized(self):
        '''
            make sure read methods returns false/nothing when the user retrieved is different from
            the logged in user
        '''
        the_bundle = mock()
        the_bundle.obj = mock()
        the_bundle.obj.pk = 1
        the_bundle.request = mock()
        the_bundle.request.user = mock()
        the_bundle.request.user.pk = 2
        self.assertFalse(self.the_auth.read_detail(None, the_bundle))
        self.assertEquals(len(list(self.the_auth.read_list(User.objects.filter(pk=1), the_bundle))),
                          0)

    def test_read_good(self):
        '''
            make sure read returns true/results when the user retrieved is the same as
            the logged in user
        '''
        the_bundle = mock()
        the_bundle.obj = mock()
        the_bundle.obj.pk = 2
        the_bundle.request = mock()
        the_bundle.request.user = mock()
        the_bundle.request.user.pk = 2
        self.assertTrue(self.the_auth.read_detail(None, the_bundle))
        self.assertTrue(self.the_auth.read_list(User.objects.filter(pk=2), the_bundle).count(),
                        1)


class OwnerObjectsOnlyAuthorizationTests(TestCase):
    ''' tests for the OwnerObjectsOnlyAuthorization class '''
    fixtures = ['users_groups_perms.json', 'cigarshops_favs.json']

    def setUp(self):
        ''' set up the test '''
        self.the_auth = OwnerObjectsOnlyAuthorization()
        self.the_bundle = mock()
        self.the_bundle.request = mock()

    def tearDown(self):
        ''' tear down the test '''
        unstub()

    def test_limit_detail(self):
        '''
            make sure methods that limit detail return false for wrong user
            and true for the right one
        '''
        self.the_bundle.request.user = User.objects.get(pk=2)
        self.the_bundle.obj = CigarShop.objects.get(pk=1)
        self.assertFalse(self.the_auth.read_detail(None, self.the_bundle))
        self.assertFalse(self.the_auth.create_detail(None, self.the_bundle))
        self.assertFalse(self.the_auth.update_detail(None, self.the_bundle))
        self.assertFalse(self.the_auth.delete_detail(None, self.the_bundle))
        self.the_bundle.request.user = User.objects.get(pk=1)
        self.assertTrue(self.the_auth.read_detail(None, self.the_bundle))
        self.assertTrue(self.the_auth.create_detail(None, self.the_bundle))
        self.assertTrue(self.the_auth.update_detail(None, self.the_bundle))
        self.assertTrue(self.the_auth.delete_detail(None, self.the_bundle))

    def test_limit_list(self):
        ''' verify that list gets filtered by owner for methods limiting a list '''
        self.the_bundle.request.user = User.objects.get(pk=2)
        object_list = CigarShop.objects.all()
        self.assertEquals(0, len(list(self.the_auth.read_list(object_list, self.the_bundle))))
        self.assertEquals(0, len(list(self.the_auth.create_list(object_list, self.the_bundle))))
        self.assertEquals(0, len(list(self.the_auth.update_list(object_list, self.the_bundle))))
        self.assertEquals(0, len(list(self.the_auth.delete_list(object_list, self.the_bundle))))
        self.the_bundle.request.user = User.objects.get(pk=1)
        self.assertEquals(2, len(list(self.the_auth.read_list(object_list, self.the_bundle))))
        self.assertEquals(2, len(list(self.the_auth.create_list(object_list, self.the_bundle))))
        self.assertEquals(2, len(list(self.the_auth.update_list(object_list, self.the_bundle))))
        self.assertEquals(2, len(list(self.the_auth.delete_list(object_list, self.the_bundle))))
