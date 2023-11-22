from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.decorators import login_required
from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .models import SportFacility

@login_required
def index(request):
    user = get_user(request)
    if user.groups.filter(name="RegularUsers").exists():
        return redirect("search")
    # TODO: redirect do odpowiedniego widoku w zależności od grupy


def make_plotly_map():
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
    fig = px.scatter_mapbox(df, lat="lat", lon="long", hover_data=["owner", "name", "type"])
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox_bounds={"west": 52, "east": 52.4, "south": 20.8, "north": 21.2})
    fig.update_traces(marker={"size":10, "color":"blue"})
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=52.2,lon=21))
    return plot(fig, output_type="div", include_plotlyjs=False)


# wyszukiwarka
def search_facilities(request):
    return render(request, "main/search.html", {"plot": make_plotly_map()})


# wszystkie obiekty sportowe danego użytkownika
def get_facilities(request, uid):
    owner = get_object_or_404(get_user_model(), pk=uid)
    facilities = get_list_or_404(SportFacility, owner=uid)
    return render(request, "main/user_facilities.html", {"owner": owner, "facilities": facilities})


# widok dla jednego obiektu - rezerwacja (RegularUsers) lub edycja (SportFacilityOwners)
def facility_detail(request, fid):
    facility = get_object_or_404(SportFacility, pk=fid)
