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
            "Geocoded {0} locations".format(len(geocoded)))
