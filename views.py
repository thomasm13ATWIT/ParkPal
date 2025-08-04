# File: C:\Users\thomasm13\parking_project_django\parking_tracker\views.py

from django.shortcuts import render  # For the optional display_car_count view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # To disable CSRF protection for API endpoints called by scripts
from django.views.decorators.http import require_POST, require_GET # To restrict HTTP methods
import json # To parse JSON data from requests
import logging # For logging messages and errors

from .models import ParkingLotStatus, Subscriber # Import the models you defined in models.py

# Get the logger instance configured in settings.py
# This allows you to see print statements from your views in the Django development server console
# if the logging level for 'parking_tracker' is set to DEBUG in settings.py.
logger = logging.getLogger(__name__)

@csrf_exempt # Disable CSRF protection for this API. For production, consider token authentication.
@require_POST # This view will only accept POST requests.
def update_car_count_api(request):
    """
    API endpoint for the Raspberry Pi's car counter script to SEND data TO Django.
    Expects a JSON payload like: {"car_count": N}
    """
    try:
        # Decode the request body from bytes to string, then parse JSON
        data = json.loads(request.body.decode('utf-8'))
        car_count = data.get('car_count') # Safely get 'car_count' from the parsed JSON

        # Validate the received car_count
        if car_count is None or not isinstance(car_count, int) or car_count < 0:
            logger.warning(f"API: Invalid car_count data received: {data}")
            return JsonResponse({'status': 'error', 'message': 'Invalid or missing car_count data. Must be a non-negative integer.'}, status=400)

        # Get the single ParkingLotStatus object (or create it if it's the first time)
        status_obj = ParkingLotStatus.get_status() # Uses the classmethod from your model
        status_obj.current_car_count = car_count
        status_obj.save() # This will also update the 'last_updated' field due to auto_now=True

        logger.info(f"API: Car count successfully updated to {car_count}.")
        return JsonResponse({'status': 'success', 'message': f'Car count updated to {car_count}.'})
    except json.JSONDecodeError:
        logger.error("API: Invalid JSON received in update_car_count_api.")
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in request body.'}, status=400)
    except Exception as e:
        # Log the full exception details for easier debugging
        logger.error(f"API: Error in update_car_count_api: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': f'An internal server error occurred: {str(e)}'}, status=500)

@require_GET # This view will only accept GET requests.
def get_lot_status_api(request):
    """
    API endpoint for the Raspberry Pi's Twilio script to GET the current car count.
    """
    try:
        status_obj = ParkingLotStatus.get_status()
        data_to_send = {
            'car_count': status_obj.current_car_count,
            'last_updated': status_obj.last_updated.isoformat() if status_obj.last_updated else None
            # isoformat() is a standard way to represent datetime as a string for APIs
        }
        return JsonResponse(data_to_send)
    except ParkingLotStatus.DoesNotExist: # Should be handled by get_status(), but good for robustness
        logger.warning("API: ParkingLotStatus object not found (get_lot_status_api).")
        return JsonResponse({'status': 'error', 'message': 'Parking lot status not found.'}, status=404)
    except Exception as e:
        logger.error(f"API: Error in get_lot_status_api: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Internal server error while fetching lot status.'}, status=500)

@require_GET # This view will only accept GET requests.
def get_active_subscribers_api(request):
    """
    API endpoint for the Raspberry Pi's Twilio script to GET active subscriber phone numbers.
    """
    try:
        # Get a list of phone numbers for all subscribers where is_active is True
        active_subscribers_phones = Subscriber.objects.filter(is_active=True).values_list('phone_number', flat=True)
        data_to_send = {
            'subscribers': list(active_subscribers_phones) # Convert QuerySet to a list
        }
        return JsonResponse(data_to_send)
    except Exception as e:
        logger.error(f"API: Error in get_active_subscribers_api: {e}", exc_info=True)
        return JsonResponse({'status': 'error', 'message': 'Internal server error while fetching subscribers.'}, status=500)

# --- Optional: A simple view to display the status on a webpage ---
def display_car_count(request):
    """
    A regular Django view to render an HTML page showing the car count.
    This is for humans to look at in a web browser, not for the Pi.
    """
    try:
        status = ParkingLotStatus.get_status()
    except Exception as e:
        logger.error(f"Display: Error fetching status for display_car_count: {e}")
        status = None # So the template can handle it gracefully

    context = {
        'lot_status': status,
        'page_title': 'Live Parking Lot Status'
    }
    # This assumes you will create a template at 'parking_tracker/car_count_display.html'
    return render(request, 'parking_tracker/car_count_display.html', context)