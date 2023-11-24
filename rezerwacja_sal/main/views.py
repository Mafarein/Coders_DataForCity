from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import pandas as pd
from .models import SportFacility, TimeSlot
from .utils import make_plotly_map
from .forms import *


@login_required
def index(request):
    user = get_user(request)
    if user.groups.filter(name="RegularUsers").exists():
        return redirect("search")
    else:
        return redirect("user_facilities", user.pk)


# wyszukiwarka
def search_facilities(request):
    facilities = SportFacility.objects.filter(is_active = True)
    f_data = [
        {
            "lat": f.latitude,
            "long": f.longitude,
            "name": f.name,
            "owner": f.owner.get_username(),
            "type": [t.type for t in f.type.iterator()]
        } for f in facilities
    ]
    # podajemy nazwy kolumn na wypadek, gdyby zbiór danych był pusty
    df = pd.DataFrame(f_data, columns=["lat", "long", "name", "owner", "type"])
    return render(request, "main/search.html", {"plot": make_plotly_map(df)})


# wszystkie obiekty sportowe danego użytkownika
def get_facilities(request, uid):
    owner = get_object_or_404(get_user_model(), pk=uid)
    facilities = SportFacility.objects.filter(owner_id=uid, is_active=True)
    return render(request, "main/user_facilities.html", {"owner": owner, "facilities": facilities})


# widok dla jednego obiektu - rezerwacja (RegularUsers) lub edycja (SportFacilityOwners)
def facility_detail(request, fid):
    facility = get_object_or_404(SportFacility, pk=fid)
    if not facility.is_active:
        raise Http404()
    timeslots = TimeSlot.objects.filter(facility_id=facility)
    return render(request, "main/facility_detail.html", {"facility": facility, "timeslots": timeslots})


def create_facility(request):
    user = get_user(request)
    if user.groups.filter(Q(name="SportFacilityOwners") | Q(name="Schools")).exists():
        if request.method == "POST":
            form = SportFacilityForm(request.POST)
            facility = form.save(user)
            # TODO: powiadom admina o próbie utworzenia obiektu
            return render(request, "main/facility_created.html")
        else:
            form = SportFacilityForm()
            return render(request, "main/create_facility.html", {"form": form})
    else:
        return HttpResponseForbidden()
