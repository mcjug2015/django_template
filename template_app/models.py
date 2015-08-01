from django.contrib.gis.db import models
from django.db import models as classic_models
from django.contrib.auth.models import User


class CigarShop(models.Model):
    ''' Model class for a cigar shop, has owner and location '''
    objects = models.GeoManager()
    name = models.CharField(max_length=250, null=False, blank=False)
    location = models.PointField()
    owner = models.ForeignKey(User, related_name='cigar_shops', null=False, blank=False)


class FaveShops(models.Model):
    ''' Model class for a bunch of shops a user likes '''
    objects = models.GeoManager()
    name = models.CharField(max_length=250, null=False, blank=False)
    owner = models.ForeignKey(User, related_name='faves', null=False, blank=False)
    cigar_shops = models.ManyToManyField(CigarShop)