# File: C:\Users\thomasm13\parking_project_django\parking_tracker\admin.py

from django.contrib import admin
from .models import ParkingLotStatus, Subscriber  # Import your models

@admin.register(ParkingLotStatus)
class ParkingLotStatusAdmin(admin.ModelAdmin):
    """
    Admin interface options for ParkingLotStatus model.
    """
    list_display = ('identifier', 'current_car_count', 'last_updated')
    # Since 'identifier' is the primary key and 'last_updated' is auto-set,
    # they are often good candidates for readonly_fields in the detail view.
    readonly_fields = ('identifier', 'last_updated')

    # Since we intend ParkingLotStatus to be a singleton-like model (only one 'MainLot' entry),
    # we can prevent users from adding new instances or deleting the existing one via the admin.
    def has_add_permission(self, request):
        # Allow adding only if no ParkingLotStatus object exists yet.
        # Adjust if you allow multiple identifiers. For 'MainLot', only one should exist.
        return ParkingLotStatus.objects.count() == 0

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of any ParkingLotStatus objects via admin.
        return False

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Admin interface options for Subscriber model.
    """
    list_display = ('phone_number', 'is_active', 'subscribed_at')
    list_filter = ('is_active',) # Adds a filter sidebar for 'is_active'
    search_fields = ('phone_number',) # Adds a search box for phone numbers

    # You can add actions to the admin interface. For example:
    actions = ['mark_as_active', 'mark_as_inactive']

    def mark_as_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_as_active.short_description = "Mark selected subscribers as active"

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_as_inactive.short_description = "Mark selected subscribers as inactive"

# Alternatively, instead of using the @admin.register decorator, you can do:
# admin.site.register(ParkingLotStatus, ParkingLotStatusAdmin)
# admin.site.register(Subscriber, SubscriberAdmin)
# Or for very basic registration without customization:
# admin.site.register(ParkingLotStatus)
# admin.site.register(Subscriber)