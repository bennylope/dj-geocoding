# -*- coding: utf-8 -*-

import decimal

from django.conf import settings
from django.db import models
from django.db.models.query import QuerySet
from geocodio import GeocodioClient

from .utils import bulk_geocode


class GeocodingQuerySet(QuerySet):
    """
    QuerySet that adds a simple geocoding method.
    """
    def geocode(self, *args, **kwargs):
        """
        Geocodes all elements in the current QuerySet, setting all the given
        fields to the appropriate values.
        """
        clone = self._clone()
        return bulk_geocode(clone, *args, **kwargs)
    geocode.alters_data = True


class GeocodingManager(models.Manager):
    """
    Manager class that provides a bulk geocoding queryset method.
    """
    def get_query_set(self):
        return GeocodingQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return GeocodingQuerySet(self.model, using=self._db)


class GeoFieldsModel(models.Model):
    """
    Mixin for models that require geolocation but do not make use of GeoDjagno
    features.
    """
    latitude = models.DecimalField(decimal_places=15, max_digits=18, null=True,
            blank=True)
    longitude = models.DecimalField(decimal_places=15, max_digits=18, null=True,
            blank=True)

    class Meta:
        abstract = True

    def _get_point(self):
        """
        :returns: tuple of the latitude, longitude of the point
        """
        return self.latitude, self.longitude

    def _set_point(self, point_tuple):
        """
        Method to set the latitude and longitude via a single tuple or list.
        The method verifies the data types right away, rather than just wait
        for the model's `save` method to clean the data.

        :returns: tuple of the latitude, longitude of the point
        """
        try:
            assert len(point_tuple) == 2
        except AssertionError:
            raise Exception("point_tuple must have exactly two elements")

        self.latitude = decimal.Decimal(str(point_tuple[0]))
        self.longitude = decimal.Decimal(str(point_tuple[1]))
        return self.latitude, self.longitude

    point = property(_get_point, _set_point)

    @property
    def has_geolocation(self):
        if self.latitude is not None and self.longitude is not None:
            return True
        return False


class GeocoderMixin(object):

    def geocode(self, *args, **kwargs):
        """
        Geocodes the object.

        Uses either a `get_display_address` method on the object or the
        arguments provided.

        :returns: the object itself
        """
        separator = kwargs.pop('separator', ', ')
        save = kwargs.pop('save', True)
        if hasattr(self, 'get_display_address'):
            address = self.get_display_address()
        elif not args:
            raise ValueError("Must provide field names for address display if no"
                    " get_display_address method is present")
        else:
            address = separator.join([getattr(self, arg) for arg in args])
        client = GeocodioClient(settings.GEOCODIO_API_KEY)
        result = client.geocode(address)
        # TODO handle None
        self.point = decimal.Decimal(str(result.coords[0])), decimal.Decimal(str(result.coords[1]))
        if save:
            self.save()
        return self.point


class GeoBase(GeoFieldsModel, GeocoderMixin):
    """
    Base model class that provides dual fields for storing latitude and
    longitude, respectively, and methods for dealing with points and geocoding.
    """

    class Meta:
        abstract = True
