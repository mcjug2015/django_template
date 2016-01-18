''' unit tests for the models '''
from django.test.testcases import TestCase
from template_app.models import CigarShop, FaveShops


class CigarShopTests(TestCase):
    ''' Tests for the cigar shop model '''
    fixtures = ['users_groups_perms.json', 'cigarshops_favs.json']

    def test_str(self):
        ''' make sure the str method returns the name '''
        self.assertEquals(str(CigarShop.objects.get(pk=1)), 'awesome cigar shop')


class FavShopsTests(TestCase):
    ''' Tests for the fave shops model '''
    fixtures = ['users_groups_perms.json', 'cigarshops_favs.json']

    def test_str(self):
        ''' make sure the str method returns the name '''
        self.assertEquals(str(FaveShops.objects.get(pk=1)), 'top cigar shops around dc')
