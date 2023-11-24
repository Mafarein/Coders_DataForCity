from django.db import models
from django.contrib.auth.models import User


class SchoolProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Nazwa szkoły", max_length=50)
    lat = models.FloatField(name="latitude")
    long = models.FloatField(name="longitude")
    street_name = models.CharField(max_length=50)
    building_number = models.PositiveSmallIntegerField()
