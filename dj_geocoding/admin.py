from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class GeocodedFilter(SimpleListFilter):
    """
    Admin list filter for filtering locations by whether they have
    [complete] geolocation data.
    """
    title = _('geocoded')
    parameter_name = 'geocoded'

    def lookups(self, request, model_admin):
        return (
            ('1', _('Yes')),
            ('0', _('No')),
        )

    def queryset(self, request, queryset):
        """
        Returns queryset of locations based on whether the locations
        have complete geolocation data (latitude and longitude) or
        those that lack complete geolocation data (none or only one).
        """
        if self.value() == '1':
            return queryset.filter(latitude__isnull=False, longitude__isnull=False)
        if self.value() == '0':
            return queryset.exclude(latitude__isnull=False, longitude__isnull=False)


class GeolocateMixin(object):
    """
    ModelAdmin class mixin for adding a simple geocoding interface to the
    Django admin.
    """
    actions = ['geocode_address']

    def geocode_address(self, request, queryset):
        """
        Make a request from Google via the Maps API to get the lat/lng
        locations for the selected locations.
        """
        try:
            geocoded = queryset.geocode()
        except AttributeError:
            # TODO Add a helpful error message here
            raise
        self.message_user(request,
            _("Geocoded {0} locations".format(len(geocoded))))
