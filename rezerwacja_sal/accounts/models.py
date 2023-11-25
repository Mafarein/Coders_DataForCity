from django.db import models
from django.contrib.auth.models import User


class SchoolProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(verbose_name="Nazwa szkoły", max_length=100)
    lat = models.FloatField(verbose_name="latitude", default=0)
    long = models.FloatField(verbose_name="longitude", default=0)
    street_name = models.CharField(max_length=50)
    building_number = models.PositiveSmallIntegerField()
