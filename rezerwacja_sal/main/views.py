from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user, get_user_model
# from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
import pandas as pd
from .models import SportFacility, TimeSlot
from .utils import make_plotly_map, is_regular_user
from .forms import *


def index(request):
    user = get_user(request)
    if is_regular_user(user) or user.is_anonymous:
        return redirect("search")
    else:
        return redirect("profile")


# wyszukiwarka
def search_facilities(request):
    search_form = FacilitySearchForm(request.GET)
    hour = search_form.data.get('hour')
    date = search_form.data.get('date')
    ts = TimeSlot.objects.all()
    if hour is not None:
        ts = ts.filter(start__lte=hour, end__gte=hour)#.select_related("facility")
    if date not in [None, ""]:
        ts = ts.filter(date=date)
    facilities = SportFacility.objects.filter(is_active = True, id__in=ts.values("facility_id"))
    if search_form.data.get('type') is not None and search_form.data.get('type') != str(SportFacilityType.objects.get(type="-----").id):
        facilities = facilities.filter(type=search_form.data['type'])
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
    return render(request, "main/search.html", {"plot": make_plotly_map(df), "search_form": search_form, "facilities": facilities})


# wszystkie obiekty sportowe danego użytkownika
def get_facilities(request, uid):
    owner = get_object_or_404(get_user_model(), pk=uid)
    facilities = SportFacility.objects.filter(owner_id=uid, is_active=True)
    return render(request, "main/user_facilities.html", {"owner": owner, "facilities": facilities})


def make_reservation(request, user, facility, timeslots):
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid(facility):
            reservation_form.save(user, facility)
            return render(request, "main/reservation_made.html")
    else:
        reservation_form = ReservationForm()
        context = {"facility": facility, "timeslots": timeslots, "reservation_form": reservation_form}
        return render(request, "main/make_reservation.html", context)
    

def facility_edit(request, fid):
    facility = get_object_or_404(SportFacility, pk=fid)
    timeslots = TimeSlot.objects.filter(facility_id=facility)

    if request.method == "POST":
        timeslot_form = TimeSlotForm(request.POST)
        if timeslot_form.is_valid():
            timeslot_form.save(facility)
    else:
        timeslot_form = TimeSlotForm()

    return render(request, "main/facility_edit.html", {"facility": facility, "timeslots": timeslots, "timeslot_form": timeslot_form})


def facility_detail(request, fid):
    facility = get_object_or_404(SportFacility, pk=fid)
    if not facility.is_active:
        raise Http404()
    timeslots = TimeSlot.objects.filter(facility_id=facility)
    user = get_user(request)
    if is_regular_user(user):
        return make_reservation(request, user, facility, timeslots)
    if facility.owner == user:
        return facility_edit(request, facility, timeslots)
    return render(request, "main/facility_detail.html", {"facility": facility, "timeslots": timeslots})


def create_facility(request):
    user = get_user(request)
    if user.groups.filter(Q(name="SportFacilityOwners") | Q(name="Schools")).exists():
        if request.method == "POST":
            form = SportFacilityForm(request.POST)
            if form.is_valid():
                facility = form.save(user)
            # TODO: powiadom admina o próbie utworzenia obiektu
            return render(request, "main/facility_created.html")
        else:
            form = SportFacilityForm()
            if user.groups.filter(name="Schools").exists():
                sp = user.school_profile
                form = SportFacilityForm({"street_name": sp.street_name, "building_number": sp.building_number})
            return render(request, "main/create_facility.html", {"form": form})
    else:
        return HttpResponseForbidden()




