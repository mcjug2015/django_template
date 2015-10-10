''' tastypie apis for the template app '''
from tastypie.contrib.gis.resources import ModelResource
from template_app.models import CigarShop, FaveShops
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization


class CigarShopResource(ModelResource):
    ''' tastypie resource for cigarshop '''
    
    class Meta(object):
        ''' meta info '''
        queryset = CigarShop.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()


class FaveShopsResource(ModelResource):
    ''' tastypie resource for faveshops '''
    
    class Meta(object):
        ''' meta info '''
        queryset = FaveShops.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
