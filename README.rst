============
dj-geocoding
============

.. image:: https://travis-ci.org/bennylope/dj-geocoding.svg?branch=master
    :target: https://travis-ci.org/bennylope/dj-geocoding

Django features for simple geocoding. Current support for the Geocodio geocoding service

Installing
==========

Install dj-geocoding::

    pip install dj-geocoding

Then use it in a project::

    import dj-geocoding

Add your geocoding service API credentials to your `settings.py` file::

    GEOCODIO_API_KEY="SOMEAPIKEY"

Model
=====

Use the optional model mixin to your model if you aren't using PostGIS::

    from dj_geocoding.models import GeoBase

    class MyModel(GeoBase, models.Model):
        pass

This adds the followng fields::

    latitude = models.DecimalField(decimal_places=15, max_digits=18, null=True,
            blank=True)
    longitude = models.DecimalField(decimal_places=15, max_digits=18, null=True,
            blank=True)

Adds a geocode method::

    def geocode(self, \*args, \**kwargs):
        return geocode()

You should extend this in your model, providing the field(s) from which the
address will be pulled::

    def geocode(self):
        return super(MyModel, self).geocode('address')

You can choose the separator for providing a single address, too::

    def geocode(self):
        return super(MyModel, self).geocode('street_address', 'city', 'state',
                seperator=", ")

And additional property attributes for the `point` attribute.

Bulk geocoding
==============

The `bulk_geocode` function takes a queryset and geocodes its member objects.

.. note::

    The model *must* implement a point-type field that behaves like a
    Point field.

Example::

    geocoded_qs = bulk_geocode(MyModel.objects.all())

Specifying the field name::

    geocoded_qs = bulk_geocode(MyModel.objects.all(), field='point')

Manager
-------

The manager class implements a subclassed `QuerySet` with a `geocode` method::

    MyModel.objects.all().geocode()

This returns a queryset of the objects updated (or not) that fit within the
limits of the geocoding service. It is a convenient interface tot he
`bulk_geocode` function.
