from django.conf import settings
from django.db import transaction
from geocodio import GeocodioClient


def bulk_geocode(qs, *args, **kwargs):
    """
    Geocodes a queryset in bulk

    The goal is to minimize the number of API calls

    :returns: the slice of the queryset provided that was geocoded.
    """
    # TODO use 'format_address' method/attribute
    client = GeocodioClient(settings.GEOCODIO_KEY)
    geocoded_addresses = client.geocode([location.address for location in qs])
    with transaction.commit_on_success():
        for location in qs:
            location.location = geocoded_addresses.addresses.get[location.address].coords
            location.save()
    # TODO return only portion of the qs that was geocoded
    return qs
