from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email",)

class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "category", "price", "date", "status",)

class WatchAdmin(admin.ModelAdmin):
    list_display = ("user", "listing",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "listing", "bid",)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Watch, WatchAdmin)