from plotly.offline import plot
import plotly.express as px
import plotly.graph_objects as go


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
    pass
