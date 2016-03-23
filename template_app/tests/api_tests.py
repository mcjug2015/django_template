''' unit tests for the api module '''
from django.db.models import Q
from django.contrib.gis.measure import D
from django.contrib.gis.geos.factory import fromstr
from django.test.testcases import TestCase
from template_app.api import CigarShopResource


class CigarShopResourceTests(TestCase):
    ''' unit tests for the cigar shop resource '''
    fixtures = ['users_groups_perms.json', 'cigarshops_favs.json']

    def setUp(self):
        ''' set up the test '''
        self.the_resource = CigarShopResource()

    def test_build_filters_empty(self):
        '''
            verify that invoking build filters and passing in nothing returns an
            empty dict
        '''
        self.assertEquals(self.the_resource.build_filters(), {})

    def test_build_filters_existing(self):
        '''
            make sure existing filters that dont have lat, long, and distance in them
            have default tastypie behavior
        '''
        self.assertEquals(self.the_resource.build_filters({'test': 'test'}), {})

    def test_build_filters_location(self):
        '''
            make sure the location filter gets built right when lat, long and distance
            are supplied
        '''
        retval = self.the_resource.build_filters({'lat': 1,
                                                  'long': 1,
                                                  'distance': 1})
        self.assertIn('custom', retval)
        self.assertEquals(retval['custom'].__class__.__name__, 'Q')

    def test_apply_filters_empty(self):
        '''
            Make sure default tastypie behaviour occurs when no custom filter is passed in
        '''
        retval = self.the_resource.apply_filters(None, {})
        self.assertEquals(retval.count(), 2)

    def test_apply_filters_custom(self):
        '''
            Verify that custom location filter applies to queryset when passed in.
        '''
        pnt = fromstr('POINT(%s %s)' % (-77, 39), srid=4326)
        the_dict = {'custom': Q(location__distance_lte=(pnt, D(mi=0.1)))}
        retval = self.the_resource.apply_filters(None, the_dict)
        self.assertEquals(retval.count(), 1)
