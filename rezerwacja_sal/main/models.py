from django.db import models
from django.contrib.auth import get_user_model


class SportFacilityType(models.Model):
    # klasa, a nie enum, żeby administrator mógł dodać nowy typ obiektu
    # w razie potrzeby oraz aby umożliwić relację M:M z obiektem sportowym
    type = models.CharField()


class SportFacility(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) ## user
    # jeden obiekt może mieć kilka zastosowań, np. boisko może mieć kosze do koszykówki
    # oraz bramki do piłki ręcznej
    type = models.ManyToManyField(SportFacilityType)
    latitude = models.IntegerField()  # user fields ??
    longitude = models.IntegerField()
    street_name = models.CharField()
    building_number = models.PositiveIntegerField()


class TimeSlot(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    start = models.TimeField()
    end = models.TimeField()
    facility = models.ForeignKey(SportFacility)
    
    class Meta:
        constraints = [
            models.constraints.CheckConstraint(check=models.Q(models.F("start") < models.F("end")))
        ]


class Reservation(models.Model):
    renting_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE) # wypożyczający
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE)
    date = models.DateField(auto_now=False, auto_now_add=False)
    start = models.TimeField()
    end = models.TimeField()
    # szczegółowy opis celu, w jakim osoba chce wypożyczyć obiekt (np. organizacja turnieju), przekazywany
    # wypożyczającym
    motivation = models.TextField(blank=True, null=True)
    # True po akceptacji wniosku przez wypożyczającego
    accepted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.constraints.CheckConstraint(check=models.Q(models.F("start") < models.F("end")))
        ]
