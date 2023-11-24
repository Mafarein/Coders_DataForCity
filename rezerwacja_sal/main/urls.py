from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('search/', search_facilities, name="search"),
    path('usr/<int:uid>/', get_facilities, name="user_facilities"),
    path('obj/create/', create_facility, name="facility_create"),
    path('obj/<int:fid>/', facility_detail, name="facility_detail"),
]