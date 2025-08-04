# File: C:\Users\thomasm13\parking_project_django\parking_tracker\models.py

from django.db import models
from django.utils import timezone # Not strictly needed for these models now, but good practice to keep if you expand

class ParkingLotStatus(models.Model):
    # We'll use a fixed primary key to ensure we only have one row
    # representing the status of our main (or only) parking lot.
    # If you were tracking multiple lots, you might use a different approach.
    identifier = models.CharField(
        max_length=100,
        default="MainLot",  # Default identifier for the single status object
        primary_key=True    # Makes this field the primary key
    )
    current_car_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(
        auto_now=True  # Automatically sets the field to now every time the object is saved
    )

    def __str__(self):
        # This is how the object will be represented in the Django admin or when printed.
        return f"{self.identifier} - Cars: {self.current_car_count} (Updated: {self.last_updated.strftime('%Y-%m-%d %H:%M:%S')})"

    @classmethod
    def get_status(cls, identifier="MainLot"):
        # A helper class method to easily get or create the status object.
        # 'cls' refers to the class itself (ParkingLotStatus).
        # 'pk' in get_or_create refers to the primary key field.
        obj, created = cls.objects.get_or_create(pk=identifier)
        if created:
            # Optionally log or print if a new status object was created
            print(f"ParkingLotStatus object for '{identifier}' created.")
        return obj

class Subscriber(models.Model):
    phone_number = models.CharField(
        max_length=20,
        unique=True,  # Ensures no duplicate phone numbers
        help_text="Phone number in E.164 format (e.g., +14155552671)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is the subscription active for receiving updates?"
    )
    subscribed_at = models.DateTimeField(
        auto_now_add=True  # Automatically sets the field to now when the object is first created
    )

    def __str__(self):
        return f"{self.phone_number} ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        # Defines extra options for the model
        ordering = ['phone_number'] # Default order when querying subscribers