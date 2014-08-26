from django.conf import settings
from django.db import transaction
from geocodio import GeocodioClient


def bulk_geocode(qs, *args, **kwargs):
    """
    Geocodes a queryset in bulk

    The goal is to minimize the number of API calls

    :returns: the slice of the queryset provided that was geocoded.
    """
    separator = kwargs.pop('separator', ', ')

    def location_name(location):
        # IF qs.model has attr 'get_display_address, use that
        if hasattr(qs.model, 'get_display_address'):
            return location.get_display_address()
        return separator.join([getattr(location, arg) for arg in args])

    client = GeocodioClient(settings.GEOCODIO_API_KEY)
    geocoded_addresses = client.geocode([location_name(location) for location in qs])
    with transaction.commit_on_success():
        for location in qs:
            location.point = geocoded_addresses.get(location_name(location)).coords
            location.save()
    # TODO return only portion of the qs that was geocoded
    return qs
