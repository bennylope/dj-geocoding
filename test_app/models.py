from django.db import models
from dj_geocoding.models import GeoBase


class SimpleTestModel(GeoBase):
    address = models.CharField(max_length=100,
        default="100 main st")
    city = models.CharField(max_length=100,
        default="Richmond")
    state = models.CharField(max_length=2,
        default="VA")


class TestModel(SimpleTestModel):
    def get_display_address(self):
        return "{0}, {1} {2}".format(self.address, self.city, self.state)
