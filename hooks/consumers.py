import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

class HookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.group_name = 'logger_group'
            
            # Add the WebSocket to the group
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

        except Exception as e:
            logging.error(f"Error during WebSocket connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Remove the WebSocket from the group
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            logging.info(f"WebSocket disconnected with code {close_code}")
        except Exception as e:
            logging.error(f"Error during WebSocket disconnect: {e}")

    async def receive(self, text_data):
        try:
            # Send the received message to all members of the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message': text_data
                }
            )

        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON received: {e}")
            await self.send(text_data=json.dumps({'status': 'error', 'message': 'Invalid JSON'}))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'status': 'success',
            'message': event['message']
        }))
    
    # This method is called from the webhook listener to forward hook data to WebSocket
    async def forward_hook(self, event):
        content = event['content']
        await self.send(text_data=json.dumps({
            'action': 'new_hook',
            'content': content
        }))
