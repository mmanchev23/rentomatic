import os
from .models import *
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, "app/index.html")

def register_view(request):
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    username = request.POST["username"]
    email = request.POST["email"]
    pin = request.POST["pin"]
    phone_number = request.POST["phone_number"]
    password = request.POST["password"]
    confirm_password = request.POST["confirm_password"]

    # First name validation
    if not first_name:
        messages.error(request, "The 'First name' field can not be empty!")
        return render(request, "app/index.html")

    # Last name validation
    if not last_name:
        messages.error(request, "The 'Last name' field can not be empty!")
        return render(request, "app/index.html")

    # Username validation
    if not username:
        messages.error(request, "The 'Username' field can not be empty!")
        return render(request, "app/index.html")

    # Email validation
    if not email:
        messages.error(request, "The 'Email' field can not be empty!")
        return render(request, "app/index.html")

    # PIN validation
    if not pin:
        messages.error(request, "The 'PIN' field can not be empty!")
        return render(request, "app/index.html")

    if len(pin) != 10:
        messages.error(request, "Your PIN should contain exactly 10 digits!")
        return render(request, "app/index.html")

    # Phone number validation
    if not phone_number:
        messages.error(request, "The 'Phone number' field can not be empty!")
        return render(request, "app/index.html")

    if len(phone_number) != 10:
        messages.error(request, "Your phone number should contain exactly 10 digits!")
        return render(request, "app/index.html")

    # Password validation
    if not password:
        messages.error(request, "The 'Password' field can not be empty!")
        return render(request, "app/index.html")

    if not confirm_password:
        messages.error(request, "The 'Confirm password' field can not be empty!")
        return render(request, "app/index.html")

    has_atleast_eight_characters = False
    has_atleast_one_digit = any(map(str.isdigit, password))
    has_atleast_one_upper = any(map(str.isupper, password))
    has_atleast_one_lower = any(map(str.islower, password))
    has_no_forbidden = False

    if len(str(password)) >= 8:
        has_atleast_eight_characters = True

    if not str(password).__contains__('!') or not str(password).__contains__('$') or not str(password).__contains__('#') or not str(password).__contains__('%'):
        has_no_forbidden = True

    if password != confirm_password:
        messages.error(request, "Passwords must match!")
        return render(request, "app/index.html")

    if not has_atleast_eight_characters:
        messages.error(request, "The password can not contain less than 8 characters!")
        return render(request, "app/index.html", )

    if not has_atleast_one_digit:
        messages.error(request, "The password should contains atleast one digit!")
        return render(request, "app/index.html")

    if not has_atleast_one_upper:
        messages.error(request, "The password should contains atleast one upper character!")
        return render(request, "app/index.html")

    if not has_atleast_one_lower:
        messages.error(request, "The password should contains atleast one lower character!")
        return render(request, "app/index.html")

    if not has_no_forbidden:
        messages.error(request, "The password should not contains '!', '$', '#' or '%'!")
        return render(request, "app/index.html")

    try:
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            pin=pin,
            phone_number=phone_number,
            password=password
        )
        
        user.save()
        login(request, user)
        messages.success(request, "You have registered successfully!")
        return HttpResponseRedirect(reverse("index"))
    except IntegrityError:
        messages.error(request, "Username already taken!")
        return render(request, "app/index.html")

def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        messages.success(request, "You have logged in successfully!")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "Invalid username and/or password!")
        return render(request, "app/index.html")

@login_required(redirect_field_name="/")
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return HttpResponseRedirect(reverse("index"))
