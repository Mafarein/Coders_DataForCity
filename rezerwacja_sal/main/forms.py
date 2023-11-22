from django import forms
from .models import SportFacility

class SportFacilityCreationForm(forms.ModelForm):
    class Meta:
        model = SportFacility
        fields = ("type", "street_name","building_number")
