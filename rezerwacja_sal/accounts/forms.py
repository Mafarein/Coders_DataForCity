from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": "nazwa użytkownika",
            "email": "email",
            "password1": "hasło",
            "password2": "powtórz hasło"
        }
    
    def save(self, commit=False):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_active = False
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
        if commit:
            user.save()
        return user


class SchoolUserCreationForm(UserCreationForm):
    # tutaj username to nazwa szkoły
    school_name = forms.CharField(max_length=50, required=True, label="Nazwa szkoły")

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
        labels = {
            "password1": "hasło",
            "password2": "powtórz hasło"
        }
    
    def save(self, commit=True):
        user = super(SchoolUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['school_name'].replace(" ", "_")
        user.groups.add(Group.objects.get(name="Schools"))
        # TODO: utworzyć instancję SchoolProfile na podstawie danych z API
        if commit:
            user.save()
        return user
    
    def is_valid(self) -> bool:
        v = super().is_valid()
        # TODO: sprawdzić, że szkoła istnieje
        return v
