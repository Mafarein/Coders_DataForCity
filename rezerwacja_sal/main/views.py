from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.decorators import login_required
from .models import SportFacility

@login_required
def index(request):
    user = get_user(request)
    if user.groups.filter(name="RegularUsers").exists():
        return redirect("search")
    # TODO: redirect do odpowiedniego widoku w zależności od grupy


# wyszukiwarka
def search_facilities(request):
    pass


# wszystkie obiekty sportowe danego użytkownika
def get_facilities(request, uid):
    owner = get_object_or_404(get_user_model(), pk=uid)
    facilities = get_list_or_404(SportFacility, owner=uid)
    return render(request, "main/user_facilities.html", {"owner": owner, "facilities": facilities})


# widok dla jednego obiektu - rezerwacja (RegularUsers) lub edycja (SportFacilityOwners)
def facility_detail(request, fid):
    facility = get_object_or_404(SportFacility, pk=fid)
