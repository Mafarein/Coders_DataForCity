from django import forms
from .models import SportFacility

class SportFacilityForm(forms.ModelForm):
    class Meta:
        model = SportFacility
        fields = ("name", "type", "street_name","building_number")
