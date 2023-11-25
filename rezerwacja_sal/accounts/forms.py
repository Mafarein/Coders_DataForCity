from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


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
    school_name = forms.CharField(max_length=50, required=True, label="Nazwa szkoły")
    username = forms.CharField(max_length=50, required=True, label="Nazwa użytkownika")
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput, label="Hasło")
    password2 = forms.CharField(max_length=50, min_length=8, required=True, widget=forms.PasswordInput, label="Powtórz hasło")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(SchoolUserCreationForm, self).save(commit=False)
        # TODO: utworzyć instancję SchoolProfile na podstawie danych z API
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name="Schools"))
        return user
    
    def is_valid(self) -> bool:
        v = super().is_valid()
        # TODO: sprawdzić, że szkoła istnieje
        return v
