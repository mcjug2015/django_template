''' Tests for the admin module '''
from django.test.testcases import TestCase
from mockito import mock
from template_app import admin


class LatLongWidgetTests(TestCase):
    ''' Test class for the admin lat long widget '''

    def setUp(self):
        ''' set up the test '''
        self.widget = admin.LatLongWidget()

    def test_decompress_with_value(self):
        ''' test invoking the decompress method with a value '''
        the_value = mock()
        the_value.coords = [1, 2]
        retval = self.widget.decompress(the_value)
        self.assertEquals(retval[0], 2)
        self.assertEquals(retval[1], 1)

    def test_decompress_no_value(self):
        ''' verify that decompressing a falsy value returns a tuple of nones '''
        self.assertEquals(self.widget.decompress([]), (None, None))
        self.assertEquals(self.widget.decompress(None), (None, None))


class LatLongFieldTests(TestCase):
    ''' tests for the admin lat long field '''

    def setUp(self):
        ''' set up the test '''
        self.the_field = admin.LatLongField()

    def test_compress_success(self):
        ''' make sure good data produces a valid point string '''
        retval = self.the_field.compress([1, 2])
        self.assertEquals(retval, 'SRID=4326;POINT(2.000000 1.000000)')

    def test_compress_no_data(self):
        ''' verify that non or empty list returns none '''
        self.assertEquals(self.the_field.compress(None), None)
        self.assertEquals(self.the_field.compress([]), None)

    def test_compress_validation_error(self):
        ''' verify that one of the first two values beeing blanky raises validation '''
        self.assertRaises(admin.forms.ValidationError, self.the_field.compress, [1, {}])
        self.assertRaises(admin.forms.ValidationError, self.the_field.compress, ['', 2])


class CigarShopAdminTests(TestCase):
    ''' tests for the cigar shop admin class '''
    
    def setUp(self):
        ''' set up the test '''
        mock_model = mock()
        mock_model._meta = None
        self.the_admin = admin.CigarShopAdmin(mock_model, None)
    
    def test_formfield_for_dbfield_regular(self):
        ''' test default behavior when field name is not 'location' '''
        db_field = mock()
        db_field.name = 'testing'
        retval = self.the_admin.formfield_for_dbfield(db_field)
        self.assertNotEquals(type(retval), admin.LatLongField)

    def test_formfield_for_dbfield_location(self):
        ''' make sure a field named location gets a latlongfield returned '''
        db_field = mock()
        db_field.name = 'location'
        retval = self.the_admin.formfield_for_dbfield(db_field)
        self.assertEquals(type(retval), admin.LatLongField)
