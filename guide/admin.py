from django.contrib import admin

# Register your models here.
# guide/admin.py
from django.contrib import admin
from .models import UserProfile, Destination, TripPlan

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'current_place')
    search_fields = ('user__username', 'current_place')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(TripPlan)
class TripPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'budget', 'days', 'transport', 'total_price')
    search_fields = ('user__username', 'destination__name')
    list_filter = ('budget', 'transport')

# Alternatively, you can use the following format without the decorator
# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Destination, DestinationAdmin)
# admin.site.register(TripPlan, TripPlanAdmin)
