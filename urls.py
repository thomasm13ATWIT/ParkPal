# File: C:\Users\thomasm13\parking_project_django\parking_tracker\urls.py

from django.urls import path
from . import views  # Imports views from the current app (parking_tracker)

app_name = 'parking_tracker'  # This defines an application namespace for your URLs.
                              # It's useful for uniquely naming URLs, e.g., 'parking_tracker:api_update_car_count'

urlpatterns = [
    # API endpoint for the Raspberry Pi's car counter script to SEND data TO Django
    path('api/car_count/update/', views.update_car_count_api, name='api_update_car_count'),

    # API endpoints for the Raspberry Pi's Twilio script to GET data FROM Django
    path('api/get_lot_status/', views.get_lot_status_api, name='api_get_lot_status'),
    path('api/get_subscribers/', views.get_active_subscribers_api, name='api_get_subscribers'),

    # Optional: URL to display the car count on a webpage
    # This will be accessible at something like /parking/status/ in your browser
    path('status/', views.display_car_count, name='display_car_count'),
]