from django.contrib.gis import admin
from template_app.models import CigarShop, FaveShops
from django import forms
from django.core import validators


'''
From http://stackoverflow.com/questions/17021852/latitude-longitude-widget-for-pointfield
'''
class LatLongWidget(forms.MultiWidget):
    """
    A Widget that splits Point input into two latitude/longitude boxes.
    """

    def __init__(self, attrs=None, date_format=None, time_format=None):
        widgets = (forms.TextInput(attrs=attrs),
                   forms.TextInput(attrs=attrs))
        super(LatLongWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return tuple(reversed(value.coords))
        return (None, None)


class LatLongField(forms.MultiValueField):
    widget = LatLongWidget
    srid = 4326

    default_error_messages = {
        'invalid_latitude' : ('Enter a valid latitude.'),
        'invalid_longitude' : ('Enter a valid longitude.'),
    }

    def __init__(self, *args, **kwargs):
        fields = (forms.FloatField(min_value=-90, max_value=90), 
                  forms.FloatField(min_value=-180, max_value=180))
        super(LatLongField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if latitude or longitude is empty
            # (possible if LatLongField has required=False).
            if data_list[0] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_latitude'])
            if data_list[1] in validators.EMPTY_VALUES:
                raise forms.ValidationError(self.error_messages['invalid_longitude'])
            # SRID=4326;POINT(1.12345789 1.123456789)
            srid_str = 'SRID=%d'%self.srid
            point_str = 'POINT(%f %f)'%tuple(reversed(data_list))
            return ';'.join([srid_str, point_str])
        return None


class CigarShopAdmin(admin.GeoModelAdmin):
    ''' Admin model for the cigar shop '''

    def formfield_for_dbfield(self, db_field, **kwargs):
        ''' total hack, but its easier to copy paste lat-long then to drag around the map. '''
        if db_field.name == 'location':
            return LatLongField()
        return super(CigarShopAdmin, self).formfield_for_dbfield(db_field, **kwargs)


class MapCigarShop(CigarShop):
    ''' proxy cigar shop used in the admin model that shows a map. '''
    class Meta():
        ''' meta info '''
        proxy = True


# Register your models here.
admin.site.register(CigarShop, CigarShopAdmin)
admin.site.register(MapCigarShop)
admin.site.register(FaveShops)
