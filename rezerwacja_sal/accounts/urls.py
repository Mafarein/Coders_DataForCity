from django.urls import path, include
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', registration_choice, name="registration_choice"),
    path('register/reg/', regular_account_creation_form, name="reg_acc_create"),
    path('register/school/', school_account_creation_form, name="school_acc_create"),
    path('register/owner/', owner_account_creation_form, name="own_acc_create"),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('profile/', profile, name="profile")
]