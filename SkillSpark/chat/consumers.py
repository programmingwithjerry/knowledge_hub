import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.utils import timezone
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer to handle real-time chat functionality.
    This consumer manages WebSocket connections, allowing users to join
    a chat room, send messages, and receive messages in real-time via
    a group channel.
    """
    async def connect(self):
        """
        Handles a WebSocket connection when a client connects.
        This method is called when a client connects to the WebSocket. It assigns
        a room name based on the `course_id` from the URL and adds the client to
        a group channel specific to that room.
        """
        self.user = self.scope['user']
        # Retrieve the course ID from the URL route parameters
        self.id = self.scope['url_route']['kwargs']['course_id']
        # Create a unique room group name based on the course ID
        self.room_group_name = f'chat_{self.id}'
        # Join the room group by adding the WebSocket channel to the group
        await self.channel_layer.group_add(
            self.room_group_name,  # The name of the room group
            self.channel_name  # The unique channel name for the WebSocket connection
        )
        # Accept the connection
        await self.accept()

    async def disconnect(self, close_code):
        """
        Handles the WebSocket disconnection when a client disconnects.
        This method is called when a client disconnects. It removes the client
        from the room group.
        """
        # Leave the room group by discarding the WebSocket channel from the group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,  # The name of the room group
            self.channel_name  # The unique channel name for the WebSocket connection
        )


    async def persist_message(self, message):
        """
        Asynchronously persists a message to the database and sends it to the WebSocket.

        This method creates a new Message record in the database associated with the current user 
        and course, and sends the message to the WebSocket for real-time communication.

        Args:
            message (str): The content of the message to be sent and saved.
        """
        # Send message to WebSocket and save to the database asynchronously
        await Message.objects.acreate(
            user=self.user,        # The user who is sending the message
            course_id=self.id,     # The course with which the message is associated
            content=message        # The content of the message
        )


    async def receive(self, text_data):
        """
        Receives a message from the WebSocket.
        This method is called when a message is received from the WebSocket.
        It parses the message and sends it to the room group for broadcasting.
        Args:
            text_data (str): The message received in JSON format from the WebSocket.
        """
        # Parse the incoming message from JSON format
        text_data_json = json.loads(text_data)
        message = text_data_json['message']  # Extract the message from the parsed data
        now = timezone.now()
        # Send the message to the room group for broadcasting to all connected clients
        await self.channel_layer.group_send(
            self.room_group_name,  # The room group to send the message to
            {
                'type': 'chat_message',  # The type of message being sent
                'message': message,  # The actual message to be sent
                'user': self.user.username,
                'datetime': now.isoformat(),
            }
        )
        # Call the persist_message method asynchronously to save the message to the database
        # and send it to the WebSocket for real-time communication.
        await self.persist_message(message)

    async def chat_message(self, event):
        """
        Receives a message from the room group and sends it to the WebSocket.

        This method is called when a message is broadcasted to the room group.
        It sends the message to the connected WebSocket.

        Args:
            event (dict): The message event containing the message data.
        """
        # Send the message to the WebSocket client
        await self.send(text_data=json.dumps(event))  # Sends the event data to the WebSocket in JSON format
