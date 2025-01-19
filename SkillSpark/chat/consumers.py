import json
from channels.generic.websocket import WebsocketConsumer

class ChatConsumer(WebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat functionality.

    This consumer accepts WebSocket connections, handles incoming messages,
    and sends them back to the WebSocket in real-time, enabling chat features.
    """

    def connect(self):
        """
        Accepts the WebSocket connection.

        This method is called when the WebSocket connection is established.
        It accepts the connection to allow communication between the client and server.
        """
        # Accept the WebSocket connection
        self.accept()

    def disconnect(self, close_code):
        """
        Handles disconnection from the WebSocket.

        This method is called when the WebSocket connection is closed. It currently does nothing.
        The `close_code` argument provides the reason for the disconnection.
        """
        pass

    def receive(self, text_data):
        """
        Receives a message from the WebSocket and sends it back to the client.

        This method is called when a message is received from the WebSocket. It extracts the
        message from the incoming data and sends it back to the WebSocket in a JSON format.

        Args:
            text_data (str): The message received from the WebSocket in JSON format.
        """
        # Parse the incoming message from JSON format
        text_data_json = json.loads(text_data)
        message = text_data_json['message']  # Extract the message from the received data

        # Send the message back to the WebSocket in JSON format
        self.send(text_data=json.dumps({'message': message}))
