from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import SportFacility
from .utils import make_plotly_map

@login_required
def index(request):
    user = get_user(request)
    if user.groups.filter(name="RegularUsers").exists():
        return redirect("search")
    # TODO: redirect do odpowiedniego widoku w zależności od grupy


# wyszukiwarka
def search_facilities(request):
    facilities = SportFacility.objects.filter(is_active = True)
    f_data = [
        {
            "lat": f.lat,
            "long": f.long,
            "name": f.name,
            "owner": f.owner.get_username(),
            "type": f.type.type
        } for f in facilities
    ]
    # podajemy nazwy kolumn na wypadek, gdyby zbiór danych był pusty
    df = pd.DataFrame(f_data, columns=["lat", "long", "name", "owner", "type"])
    return render(request, "main/search.html", {"plot": make_plotly_map(df)})


# wszystkie obiekty sportowe danego użytkownika
def get_facilities(request, uid):
    owner = get_object_or_404(get_user_model(), pk=uid)
    facilities = get_list_or_404(SportFacility, owner=uid)
    return render(request, "main/user_facilities.html", {"owner": owner, "facilities": facilities})


# widok dla jednego obiektu - rezerwacja (RegularUsers) lub edycja (SportFacilityOwners)
def facility_detail(request, fid):
    facility = get_object_or_404(SportFacility, pk=fid)
