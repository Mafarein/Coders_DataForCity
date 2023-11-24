from typing import Any
from django import forms
from .models import SportFacility, Reservation
from .utils import get_lat_long_from_address
import datetime as dt


class SportFacilityForm(forms.ModelForm):
    class Meta:
        model = SportFacility
        fields = ("name", "type", "street_name","building_number")
        labels = {
            "name": "Nazwa",
            "type": "Typ",
            "street_name": "Nazwa ulicy",
            "building_number": "Numer budynku"
        }

    def save(self, user, commit = True) -> Any:
        fac = super().save(False)
        fac.owner = user
        fac.is_active = False
        lat, long = get_lat_long_from_address(
            self.cleaned_data['street_name'],
            self.cleaned_data['building_number'])
        if lat is None:
            return
        fac.latitude, fac.longitude = lat, long
        if commit:
            fac.save()
        return fac


HOUR_CHOICES = [(dt.time(hour=h, minute=m), f'{h:02d}:{m:02d}') for h in range(0, 24) for m in (0, 30)]


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput, required=True)
    start = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES))
    duration = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES), label="Czas trwania")
    field_order = ["date", "start", "duration", "motivation"]

    class Meta:
        model = Reservation
        fields = ("date", "start", "motivation")
        labels = {
            "date": "Data",
            "start": "Rozpoczęcie",
            "motivation": "Motywacja",
        }
        help_texts = {"motivation": "Opcjonalne szczegóły dotyczące celu, w jakim chcesz zarezerwować obiekt."}
