from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('search/', search_facilities, name="search"),
    path('obj/<int:pk>/', get_facilities, name="facility_detail"),
]