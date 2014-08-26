#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dj-geocoding
------------

Tests for `dj-geocoding` models module.
"""

import unittest
from mock import patch, MagicMock

from dj_geocoding import utils
from test_app.models import SimpleTestModel, TestModel


class TestUtils(unittest.TestCase):

    def setUp(self):
        for i in range(3):
            SimpleTestModel.objects.create()
            TestModel.objects.create()

    @patch('dj_geocoding.utils.GeocodioClient.geocode')
    def test_geocode(self, mocked_geocode):
        mocked_result = MagicMock()
        mocked_result.coords = (12, 18)
        mocked_result.get().coords = (12, 18)
        mocked_geocode.return_value = mocked_result

        qs = utils.bulk_geocode(TestModel.objects.all())
        self.assertTrue(qs[0].latitude)
