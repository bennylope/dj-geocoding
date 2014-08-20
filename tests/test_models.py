#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-geocoding
------------

Tests for `dj-geocoding` models module.
"""

import unittest
from mock import patch, MagicMock

from decimal import Decimal
from dj_geocoding import models


class TestMixins(unittest.TestCase):

    def test_point_types(self):
        """Ensure point setter only accepts numeric types"""
        geo = models.GeoFieldsMixin()
        # Floats
        geo.point = (123.12, 123.12)
        # Ints
        geo.point = (123, 123)
        # Decimals
        geo.point = (Decimal('123'), Decimal('123'))
        # Anything else
        with self.assertRaises(TypeError):
            geo.point = ('123', 123)

    @patch('dj_geocoding.models.GeocodioClient.geocode')
    def test_geocode(self, mocked_geocode):
        """Ensure that geocoding works with various address arguments"""

        mocked_result = MagicMock()
        mocked_result.coords = (12, 18)
        mocked_geocode.return_value = mocked_result

        # This could probably be mocked as well
        class PointTest(models.GeocoderMixin):
            point = None
            address = "100 main st"

        class CoolPointTest(PointTest):

            def get_display_address(self):
                return "w00t"

        # No method, but args supplied
        geotest = PointTest()
        result = geotest.geocode('address', save=False)
        self.assertEqual(result.point, (12, 18))

        # If present, called
        geotest = CoolPointTest()
        result = geotest.geocode(save=False)
        self.assertEqual(result.point, (12, 18))

        # If not present, not called
        geotest = PointTest()
        with self.assertRaises(ValueError):
            geotest.geocode(save=False)

        # If present and args sent, args ignored
        geotest = CoolPointTest()
        geotest.geocode('kjdj', save=False)
        # Test that get_display_address was called