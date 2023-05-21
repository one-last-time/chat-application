import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync

class chatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.channel_layer.group_send(self.room_group_name,
            {
                'type': 'chat.message',
                'message': ':'.join([str(x) for x in self.scope.get('client')])+' has joined the chat',
            })

    async def disconnect(self, code):
       await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, text_data):
        text_data_json = text_data
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat.message",
                "message": message
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        await self.send_json(content={"message": message})
