from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import *
from .tokens import account_activation_token
from main.models import Reservation


def account_creation_form(request, form_class):
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            msg  =render_to_string("accounts/registration_token_email.html",
                {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
                })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage("Link aktywacyjny konta", msg, to=[to_email])
            email.send()
            return render(request, "accounts/registration_token_sent.html")
    else:
        form = form_class()
    return render(request, "accounts/register.html", {"register_form": form})


def regular_account_creation_form(request):
    return account_creation_form(request, RegularUserCreationForm)


def school_account_creation_form(request):
    return account_creation_form(request, SchoolUserCreationForm)


def owner_account_creation_form(request):
    return account_creation_form(request, SportFacilityOwnerCreationForm)


def activate(request, uidb64, token):
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None 
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        return render(request, "accounts/registration_complete.html")
    return render(request, "accounts/invalid_token.html")


def registration_choice(request):
    return render(request, "accounts/registration_choice.html")


@login_required
def profile(request):
    usr = get_user(request)
    if usr.groups.filter(Q(name="SportFacilityOwners") | Q(name="Schools")).exists():
        return redirect("user_facilities", uid=usr.id)
    else:
        reservations = Reservation.objects.filter(renting_user=usr).order_by('-date')
    return render(request, "accounts/profile.html", {"user": get_user(request), "reservations": reservations})
