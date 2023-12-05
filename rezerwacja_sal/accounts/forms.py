from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import SchoolProfile
from main.utils import school_address, get_lat_long_from_address


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True, label="Nazwa użytkownika")
    first_name = forms.CharField(max_length=50, required=False, label="Imię")
    last_name = forms.CharField(max_length=50, required=False, label="Nazwisko")
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput, label="Powtórz hasło")

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    
    def save(self, commit=False):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
        return user


class RegularUserCreationForm(CustomUserCreationForm):
    def save(self, commit=True):
        user = super(RegularUserCreationForm, self).save(commit=False)
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name="RegularUsers"))
        return user
    
# konta wynajmujących: utworzenie konta nie będzie zatwierdzane przez administratora,
# ale dodanie konkretnego obiektu, którego istnienie można sprawdzić już tak

class SportFacilityOwnerCreationForm(CustomUserCreationForm):
    def save(self, commit=True):
        user = super(SportFacilityOwnerCreationForm, self).save(commit=False)
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name="SportFacilityOwners"))
        return user


class SchoolUserCreationForm(UserCreationForm):
    # tutaj username to nazwa szkoły
    school_name = forms.CharField(max_length=100, required=True, label="Nazwa szkoły")
    username = forms.CharField(max_length=50, required=True, label="Nazwa użytkownika")
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput, label="Powtórz hasło")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(SchoolUserCreationForm, self).save(commit=False)
        addr = school_address(self.cleaned_data['school_name'])
        lat, long = get_lat_long_from_address(addr['street'], addr['building_number'])
        sp = SchoolProfile(
            user=user,
            name=addr['school_name'],
            street_name=addr['street'],
            building_number=addr['building_number'],
            lat=lat,
            long=long)
        if commit:
            user.save()
            sp.save()
            user.groups.add(Group.objects.get(name="Schools"))
        return user
    
    def is_valid(self) -> bool:
        if not super().is_valid():
            return False
        sa = school_address(self.cleaned_data['school_name'])
        if sa is None:
            return False
        lat, _ = get_lat_long_from_address(sa['street'], sa['building_number'])
        return lat is not None
