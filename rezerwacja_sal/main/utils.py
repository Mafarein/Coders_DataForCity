from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go
import requests


def make_plotly_map(df):
    hoverdata = [c for c in df.columns if c != "lat" and c != "long"]
    fig = px.scatter_mapbox(df, lat="lat", lon="long", hover_data=hoverdata)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_layout(mapbox_bounds={"west": 52, "east": 52.4, "south": 20.8, "north": 21.2})
    fig.update_traces(marker={"size":10, "color":"blue"})
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=52.2,lon=21))
    return plot(fig, output_type="div", include_plotlyjs=False)


def get_lat_long_from_address(street_name, building_number):
    geocoding_url = "https://geocode.maps.co/search"
    r = requests.get(geocoding_url, params={"q": " ".join([str(building_number), street_name, "Warszawa", "PL"])})
    if not r.ok:
        return None, None
    jresponse = r.json()
    if jresponse:
        return float(jresponse[0]['lat']), float(jresponse[0]['lon'])
    else:
        return None, None


def school_address(school_name):
    school_name = school_name.upper()
    url = "https://api.um.warszawa.pl/api/action/datastore_search?"
    q = {"resource_id":"1cae4865-bb17-4944-a222-0d0cdc377951", "q":school_name}
    response = requests.get(url, q)
    if response.status_code != 200:
        return None
    data = response.json()        
    records = data['result']['records']
    if len(records) != 1:
        return None
    school = records[0]
    return {
        'school_name' : school_name,
        'street' : school.get('Ulica', None),
        'building_number' : school.get('Nr domu', None),
        'postal_code' : school.get('Kod pocztowy', None)
    }


def is_regular_user(user):
    return user.groups.filter(name="RegularUsers").exists()
