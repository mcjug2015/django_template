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
