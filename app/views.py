from pyexpat import model
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

def sign_up(request):
    return render(request, "app/sign_up.html")

def sign_up_submit(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        pin = request.POST["pin"]
        phone_number = request.POST["phone_number"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if not first_name:
            messages.error(request, "The 'First name' field can not be empty!")
            return render(request, "app/sign_up.html")

        # Last name validation
        if not last_name:
            messages.error(request, "The 'Last name' field can not be empty!")
            return render(request, "app/sign_up.html")

        # Username validation
        if not username:
            messages.error(request, "The 'Username' field can not be empty!")
            return render(request, "app/sign_up.html")

        # Email validation
        if not email:
            messages.error(request, "The 'Email' field can not be empty!")
            return render(request, "app/sign_up.html")

        # PIN validation
        if not pin:
            messages.error(request, "The 'PIN' field can not be empty!")
            return render(request, "app/sign_up.html")

        if len(pin) != 10:
            messages.error(request, "Your PIN should contain exactly 10 digits!")
            return render(request, "app/sign_up.html")

        # Phone number validation
        if not phone_number:
            messages.error(request, "The 'Phone number' field can not be empty!")
            return render(request, "app/sign_up.html")

        if len(phone_number) != 10:
            messages.error(request, "Your phone number should contain exactly 10 digits!")
            return render(request, "app/sign_up.html")

        # Password validation
        if not password:
            messages.error(request, "The 'Password' field can not be empty!")
            return render(request, "app/sign_up.html")

        if not confirm_password:
            messages.error(request, "The 'Confirm password' field can not be empty!")
            return render(request, "app/sign_up.html")

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
            return render(request, "app/sign_up.html")

        if not has_atleast_eight_characters:
            messages.error(request, "The password can not contain less than 8 characters!")
            return render(request, "app/sign_up.html", )

        if not has_atleast_one_digit:
            messages.error(request, "The password should contains atleast one digit!")
            return render(request, "app/sign_up.html")

        if not has_atleast_one_upper:
            messages.error(request, "The password should contains atleast one upper character!")
            return render(request, "app/sign_up.html")

        if not has_atleast_one_lower:
            messages.error(request, "The password should contains atleast one lower character!")
            return render(request, "app/sign_up.html")

        if not has_no_forbidden:
            messages.error(request, "The password should not contains '!', '$', '#' or '%'!")
            return render(request, "app/sign_up.html")

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
            return render(request, "app/sign_up.html")
    else:
        return render(request, "app/sign_up.html")

def sign_in(request):
    return render(request, "app/sign_in.html")

def sign_in_submit(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        try:
            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You have signed in successfully!")
            return HttpResponseRedirect(reverse("index"))
        except:
            messages.error(request, "Invalid username and/or password.")
            return render(request, "app/sign_in.html")
    else:
        return render(request, "app/sign_in.html")

@login_required(redirect_field_name="sign_in/")
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return HttpResponseRedirect(reverse("index"))

@login_required(redirect_field_name="sign_in/")
def profile(request, username):
    user = User.objects.get(username=username) or None
    profile = User.objects.get(pk=request.user.pk) or None

    likes = ProfileLike.objects.filter(user=user) or None
    like = ProfileLike.objects.filter(user=user, profile=profile) or None

    followers = ProfileFollower.objects.filter(user=user) or None
    follower = ProfileFollower.objects.filter(user=user, profile=profile) or None

    followings = ProfileFollower.objects.filter(profile=user) or None

    context = {
        "user": user,

        "likes": likes,
        "like": like,

        "followers": followers,
        "follower": follower,

        "followings": followings,
    }

    return render(request, "app/profile.html", context)

@login_required(redirect_field_name="sign_in/")
def like_profile(request, username):
    user = User.objects.get(username=username) or None
    profile = User.objects.get(pk=request.user.pk) or None
    like = ProfileLike.objects.create(user=user, profile=profile)
    messages.success(request, f"You liked {username}'s profile!")
    return HttpResponseRedirect(reverse("profile", kwargs={ "username": username }))

@login_required(redirect_field_name="sign_in/")
def dislike_profile(request, username):
    user = User.objects.get(username=username) or None
    profile = User.objects.get(pk=request.user.pk) or None
    like = ProfileLike.objects.get(user=user, profile=profile)
    like.delete()
    messages.success(request, f"You disliked {username}'s profile!")
    return HttpResponseRedirect(reverse("profile", kwargs={ "username": username }))

@login_required(redirect_field_name="sign_in/")
def follow_profile(request, username):
    user = User.objects.get(username=username) or None
    profile = User.objects.get(pk=request.user.pk) or None
    follower = ProfileFollower.objects.create(user=user, profile=profile)
    messages.success(request, f"You followed {username}!")
    return HttpResponseRedirect(reverse("profile", kwargs={ "username": username }))

@login_required(redirect_field_name="sign_in/")
def unfollow_profile(request, username):
    user = User.objects.get(username=username) or None
    profile = User.objects.get(pk=request.user.pk) or None
    follower = ProfileFollower.objects.get(user=user, profile=profile)
    follower.delete()
    messages.success(request, f"You unfollowed {username}!")
    return HttpResponseRedirect(reverse("profile", kwargs={ "username": username }))

@login_required(redirect_field_name="sign_in/")
def profile_edit(request, username):
    user = User.objects.get(pk=request.user.pk) or None

    context = {
        "user": user,
        "join_date": user.date_joined.date(),
    }

    return render(request, "app/profile_edit.html", context)

@login_required(redirect_field_name="sign_in/")
def profile_edit_submit(request, username):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk) or None

        # Profile Credentials
        username = request.POST.get("username")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        if "img" in request.FILES:
            profile_picture = request.FILES["img"]
        else:
            profile_picture = user.profile_picture

        # Password Credentials
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        # Address Credentials
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        # Social Platforms Credentials
        facebook = request.POST.get("facebook")
        instagram = request.POST.get("instagram")
        twitter = request.POST.get("twitter")

        # Job & Numbers Credentials
        job = request.POST.get("job")
        phone_number = request.POST.get("phone_number")

        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        
        user.profile_picture = profile_picture

        context = {
            "user": user,
        }

        if current_password:
            if new_password:
                if confirm_password:
                    if user.check_password(current_password):
                        if new_password == confirm_password:
                            user.set_password(new_password)
                            user.save()
                            messages.success(request, "Password updated successfully!")
                            return HttpResponseRedirect(reverse("profile", kwargs=context))
                        else:
                            messages.error(request, "Passwords should match!")
                            return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
                    else:
                        messages.error(request, "That's not your current password!")
                        return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
                else:
                    messages.error(request, "'Confirm Password' field can not be empty!")
                    return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
            else:
                messages.error(request, "'New Password' field can not be empty!")
                return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
        else:
            pass

        
        user.city = city
        user.state = state
        user.country = country

        user.facebook = facebook
        user.instagram = instagram
        user.twitter = twitter
        
        user.job = job
        user.phone_number = phone_number

        user.save()

        messages.success(request, "Changes saved successfully!")
        return HttpResponseRedirect(reverse("index"))
    else:
        messages.error(request, "An error occured!")
        return HttpResponseRedirect(reverse("index"))

@login_required(redirect_field_name="sign_in/")
def profile_delete(request, username):
    return render(request, "app/profile_delete.html")

@login_required(redirect_field_name="sign_in/")
def profile_delete_submit(request, username):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk) or None

        password = request.POST.get("password")

        context = {
            "user": user,
        }

        if user.check_password(password):
            user.delete()
            messages.success(request, "Profile deleted successfully!")
            return HttpResponseRedirect(reverse("index"))
        else:
            messages.error(request, "Wrong password!")
            return HttpResponseRedirect(reverse("profile_edit", kwargs=context))
    else:
        messages.error(request, "An error occured!")
        return HttpResponseRedirect(reverse("profile_edit", kwargs=context))

@login_required(redirect_field_name="sign_in/")
def cars(request):
    cars = Car.objects.all() or None

    context = {
        "cars": cars,
    }

    return render(request, "app/cars.html", context)

@login_required(redirect_field_name="sign_in/")
def car_apply(request, id):
    if request.method == "POST":
        user = User.objects.get(pk=request.user.pk) or None
        car = Car.objects.get(pk=id) or None
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        application = Application.objects.create(user=user, car=car, start_date=start_date, end_date=end_date)
        application.save()
        messages.success(request, f"You have applied for {car.brand} {car.model} successfully!")
        return HttpResponseRedirect(reverse("cars"))
    else:
        return render(request, "app/cars.html")

@login_required(redirect_field_name="sign_in/")
def car_create(request):
    if request.method == "POST":
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        year = request.POST.get("year")
        seats = request.POST.get("seats")
        price = request.POST.get("price")

        car = Car.objects.create(
            brand=brand,
            model=model,
            year=year,
            seats=seats,
            price=price
        )

        car.save()
        messages.success(request, f"{brand} {model} created successfully!")
        return HttpResponseRedirect(reverse("cars"))
    else:
        return render(request, "app/cars.html")

@login_required(redirect_field_name="sign_in/")
def car_edit(request, id):
    if request.method == "POST":
        car = Car.objects.get(pk=id) or None
        
        brand = request.POST.get("brand")
        model = request.POST.get("model")
        year = request.POST.get("year")
        seats = request.POST.get("seats")
        price = request.POST.get("price")

        car.brand = brand
        car.model = model
        car.year = year
        car.seats = seats
        car.price = price

        car.save()

        messages.success(request, f"{car.brand} {car.model} updated successfully!")
        return HttpResponseRedirect(reverse("cars"))
    else:
        return render(request, "app/cars.html")

@login_required(redirect_field_name="sign_in/")
def car_delete(request, id):
    if request.method == "POST":
        car = Car.objects.get(pk=id) or None
        car.delete()
        messages.success(request, f"{car.brand} {car.model} deleted successfully!")
        return HttpResponseRedirect(reverse("cars"))
    else:
        return render(request, "app/cars.html")
