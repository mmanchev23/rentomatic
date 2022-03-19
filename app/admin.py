from .models import *
from django.contrib import admin



admin.site.site_header = "Rentomatic - Admin Panel"

class ProfileLikeAdmin(admin.ModelAdmin):
    list_display = ("user", "profile")

class ProfileFollowerAdmin(admin.ModelAdmin):
    list_display = ("user", "profile")

admin.site.register(User)
admin.site.register(Car)
admin.site.register(Application)
admin.site.register(ProfileLike, ProfileLikeAdmin)
admin.site.register(ProfileFollower, ProfileFollowerAdmin)
