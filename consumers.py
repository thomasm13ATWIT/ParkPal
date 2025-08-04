# parking_tracker/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
import cv2
import numpy as np

class ParkingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'parking_updates' # A common group name for all clients

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        print("WebSocket connected for parking updates.")
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'message': 'Connected to parking updates.'
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("WebSocket disconnected from parking updates.")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'car_count_update':
            car_count = text_data_json.get('count')
            frame_base64 = text_data_json.get('frame') # Get the base64 image if sent

            print(f"Received car count: {car_count}")

            if frame_base64:
                try:
                    # Decode base64 image
                    img_bytes = base64.b64decode(frame_base64)
                    np_arr = np.frombuffer(img_bytes, np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                    # Optional: Process or save the image on the server side
                    # cv2.imwrite(f"received_frame_{car_count}.jpg", frame)
                    # print(f"Saved frame with {car_count} cars.")

                except Exception as e:
                    print(f"Error decoding frame: {e}")

            # Re-broadcast the car count (and potentially the frame) to all web clients
            # Web clients will update their display
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'send_car_count', # This will call the send_car_count method below
                    'count': car_count,
                    'frame': frame_base64 # Re-send frame if you want browser to display it
                }
            )
        else:
            print(f"Received unknown message type: {message_type}")

    async def send_car_count(self, event):
        """Called when a message is sent to the group."""
        car_count = event['count']
        frame_base64 = event.get('frame') # Get frame if available

        # Send this data to the WebSocket client (the browser)
        await self.send(text_data=json.dumps({
            'type': 'car_count_update',
            'count': car_count,
            'frame': frame_base64 # Include frame for browser if needed
        }))