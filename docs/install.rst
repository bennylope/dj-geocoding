=======================
Installing dj-geocoding
=======================

Install the package and add it to your project's requirements file::

    pip install dj-geocoding

The app does not install any models so there's no need to add to your own
project's `INSTALLED_APPS` list.

Configuration
=============

For bulk geocoding the app currently uses `Geocodio <https://geocod.io>`_.
Future versions are expected to support additional bulk geocoding services.

Add your API key to your project settings::

    GEOCODIO_API_KEY = 'jskd823jqjdkjdj191'

.. note::
    Ensure that this key is added to either a non-source controlled settings
    file or better yet is loaded via an environment variable. Secrets like this
    should never go in source control.

App configuration
=================

See :doc:`configuring admin-based geocoding <admin>` for project
integration guidance.
