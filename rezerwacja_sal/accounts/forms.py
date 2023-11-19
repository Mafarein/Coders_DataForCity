from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        return user


class RegularUserCreationForm(CustomUserCreationForm):    
    def save(self, commit=True):
        user = super(RegularUserCreationForm, self).save(commit=False)
        user.groups.add(Group.objects.get(name="RegularUsers"))
        if commit:
            user.save()
        return user
    
# konta wynajmujących: utworzenie konta nie będzie zatwierdzane przez administratora,
# ale dodanie konkretnego obiektu, którego istnienie można sprawdzić już tak

class SportFacilityOwnerCreationForm(CustomUserCreationForm):
    def save(self, commit=True):
        user = super(SportFacilityOwnerCreationForm, self).save(commit=False)
        user.groups.add(Group.objects.get(name="SportFacilityOwners"))
        user.is_active = False # do zatwierdzenia przez administratora
        if commit:
            user.save()
        return user


class SchoolUserCreationForm(UserCreationForm):
    # tutaj username to nazwa szkoły
    
    def save(self, commit=True):
        user = super(SchoolUserCreationForm, self).save(commit=False)
        user.groups.add(Group.objects.get(name="Schools"))
        # TODO: sprawdzić, że szkoła istnieje
        if commit:
            user.save()
        return user
