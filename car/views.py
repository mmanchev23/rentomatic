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
    return render(request, "car/index.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
