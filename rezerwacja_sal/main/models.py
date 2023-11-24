from django.db import models
from django.contrib.auth import get_user_model


class SportFacilityType(models.Model):
    # klasa, a nie enum, żeby administrator mógł dodać nowy typ obiektu
    # w razie potrzeby oraz aby umożliwić relację M:M z obiektem sportowym
    type = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.type


class SportFacility(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="facilities") ## user
    # opcjonalna, służy rozróżnieniu obiektów tego samego typu
    name = models.CharField("nazwa", max_length=50, null=True)
    # jeden obiekt może mieć kilka zastosowań, np. boisko może mieć kosze do koszykówki
    # oraz bramki do piłki ręcznej
    type = models.ManyToManyField(SportFacilityType)
    latitude = models.IntegerField()  # user fields ??
    longitude = models.IntegerField()
    street_name = models.CharField("nazwa ulicy", max_length=100)
    building_number = models.PositiveIntegerField("numer budynku")
    # is_active - czy obiekt został zatwierdzony przez administrację?
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.owner) +" "+ self.name


class TimeSlot(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    start = models.TimeField()
    end = models.TimeField()
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name="timeslots")
    
    class Meta:
        constraints = [
            models.constraints.CheckConstraint(check=models.Q(start__lte = models.F("end")), name="timeslot_start_leq_end")
        ]


class Reservation(models.Model):
    renting_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="reservations") # wypożyczający
    facility = models.ForeignKey(SportFacility, on_delete=models.CASCADE, related_name="reservations")
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
            models.constraints.CheckConstraint(check=models.Q(start__lte = models.F("end")), name="reservation_start_leq_end")
        ]
