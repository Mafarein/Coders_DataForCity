from typing import Any
from django import forms
from .models import SportFacility
from .utils import get_lat_long_from_address


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
