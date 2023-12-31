from typing import Any
from django import forms
from django.db.models import Q
from .models import SportFacility, Reservation, TimeSlot
from .utils import get_lat_long_from_address, get_all_facility_types
import datetime as dt


HOUR_CHOICES = [(dt.time(hour=h, minute=m), f'{h:02d}:{m:02d}') for h in range(0, 24) for m in (0, 30)]
NULL_CHOICE = (None, "-----")


class SportFacilityForm(forms.ModelForm):
    class Meta:
        model = SportFacility
        fields = ("name", "type", "street_name","building_number", "description")
        labels = {
            "name": "Nazwa",
            "type": "Typ",
            "street_name": "Nazwa ulicy",
            "building_number": "Numer budynku",
            "description": "Opis"
        }
        help_texts = {
            "type": "Wciśnij CTRL, aby wybrać kilka opcji."
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


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput, required=True)
    start = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES), required=True, label="Rozpoczęcie")
    duration = forms.DurationField(widget=forms.Select(choices=HOUR_CHOICES), label="Czas trwania", required=True, help_text="Proszę zwróć uwagę że jest to czas trwania, a nie godzina zakończenia")
    field_order = ["date", "start", "duration", "motivation"]

    class Meta:
        model = Reservation
        fields = ("date", "start", "motivation")
        labels = {"motivation": "Motywacja"}
        help_texts = {
            "duration": "Uwaga: z przyczyn technicznych rezerwacja zostanie odrzucona, "
                "jeżeli skończy się po północy następnego dnia. Aby zarezerwować obiekt na noc, "
                "należy utworzyć dwie rezerwacje: jedną trwającą do północy, a drugą rozpoczynającą się o północy.",
            "motivation": "Opcjonalne szczegóły dotyczące celu, w jakim chcesz zarezerwować obiekt."
            }

    def get_end_time(self):
        start_dt = dt.datetime.combine(self.cleaned_data['date'], self.cleaned_data['start'])
        end_dt = start_dt + self.cleaned_data['duration']
        if end_dt.date() == start_dt.date():
            return end_dt.time()
        return None

    def save(self, user, facility, commit=True):
        reservation = super().save(False)
        reservation.end = self.get_end_time()
        reservation.renting_user = user
        reservation.facility = facility
        reservation.accepted = False
        if commit:
            reservation.save()
        return reservation

    def is_valid(self, facility) -> bool:
        if not super().is_valid():
            return False
        # 1. timeslot exists
        end = self.get_end_time()
        if end is None:
            return False
        ts = TimeSlot.objects.filter(
            date=self.cleaned_data['date'],
            facility=facility,
            start__lte=self.cleaned_data['start'],
            end__gte=end
            ).exists()
        # 2. clashing reservations
        clashing = Reservation.objects.filter(
            (Q(start__lt=end) & Q(start__gte=self.cleaned_data['start'])) | (Q(end__gt=self.cleaned_data['start']) & Q(end__lte=end)),
            date=self.cleaned_data['date'],
            facility=facility,
            accepted=True
        ).exists()
        return ts and not clashing


class TimeSlotForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput, label="Data", required=True)
    start = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES), label="Początek", required=True)
    end = forms.TimeField(widget=forms.Select(choices=HOUR_CHOICES), label="Koniec", required=True)

    class Meta:
        model = TimeSlot
        fields = ("date", "start", "end")

    def is_valid(self) -> bool:
        return super().is_valid() and self.cleaned_data['start'] < self.cleaned_data['end']
    
    def save(self, facility, commit=True):
        ts = super().save(commit=False)
        ts.facility = facility
        if commit:
            ts.save()
        return ts


class FacilitySearchForm(forms.Form):
    type = forms.ChoiceField(choices=lambda: [NULL_CHOICE]+get_all_facility_types(), initial=NULL_CHOICE[1], label="Typ", required=False)
    date = forms.DateField(widget=DateInput, label="Data", required=False)
    hour = forms.ChoiceField(choices=[NULL_CHOICE]+HOUR_CHOICES, initial=NULL_CHOICE[1], label="Godzina", required=False)
