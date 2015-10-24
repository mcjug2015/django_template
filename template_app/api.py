# pylint: disable=E1101
''' tastypie apis for the template app '''
from tastypie.contrib.gis.resources import ModelResource
from template_app.models import CigarShop, FaveShops
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from django.contrib.gis.geos.factory import fromstr
from django.db.models import Q
from django.contrib.gis.measure import D


class CigarShopResource(ModelResource):
    ''' tastypie resource for cigarshop '''

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(CigarShopResource, self).build_filters(filters)

        if 'lat' in filters and 'long' in filters and 'distance' in filters:
            pnt = fromstr('POINT(%s %s)' % (filters['long'], filters['lat']), srid=4326)
            orm_filters.update({'custom': Q(location__distance_lte=(pnt, D(mi=filters['distance'])))})

        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None

        semi_filtered = super(CigarShopResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered

    class Meta(object):
        ''' meta info '''
        queryset = CigarShop.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        filtering = {'location': ALL}


class FaveShopsResource(ModelResource):
    ''' tastypie resource for faveshops '''

    class Meta(object):
        ''' meta info '''
        queryset = FaveShops.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
