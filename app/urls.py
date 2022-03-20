
from .views import *
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Index Route
    path("", index, name="index"),

    # Admin Route
    path("admin/", admin.site.urls, name="admin"),

    # Register Routes
    path("sign-up/", sign_up, name="sign_up"),
    path("sign-up/submit/", sign_up_submit, name="sign_up_submit"),

    # Log In Routes
    path("sign-in/", sign_in, name="sign_in"),
    path("sign-in/submit/", sign_in_submit, name="sign_in_submit"),
    path("logout/", logout_view, name="logout"),

    # Profile Routes
    path("profile/<str:username>/", profile, name="profile"),
    path("profile/<str:username>/like/", like_profile, name="like_profile"),
    path("profile/<str:username>/dislike/", dislike_profile, name="dislike_profile"),
    path("profile/<str:username>/follow/", follow_profile, name="follow_profile"),
    path("profile/<str:username>/unfollow/", unfollow_profile, name="unfollow_profile"),

    # Profile Settings Routes
    path("profile/<str:username>/settings/", profile_edit, name="profile_edit"),
    path("profile/<str:username>/settings/submit/", profile_edit_submit, name="profile_edit_submit"),
    
    # Profile Delete Routes
    path("profile/<str:username>/delete/", profile_delete, name="profile_delete"),
    path("profile/<str:username>/delete/submit/", profile_delete_submit, name="profile_delete_submit"),

    
    # Cars routing
    path("cars/", cars, name="cars"),
    path("car/create/", car_create, name="car_create"),
    path("car/<uuid:id>/apply/", car_apply, name="car_apply"),
    path("car/<uuid:id>/edit/", car_edit, name="car_edit"),
    path("car/<uuid:id>/delete/", car_delete, name="car_delete"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)