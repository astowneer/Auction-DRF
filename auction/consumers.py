import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import Auction
from asgiref.sync import sync_to_async

class BidConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.auction_id = self.scope["url_route"]["kwargs"]["auction_id"]
        self.room_group_name = f"auction_{self.auction_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        bid = text_data_json["bid"]
        
        auction = await sync_to_async(Auction.objects.get)(id=self.auction_id)
        remaining_time = (auction.finished - timezone.now()).total_seconds()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "bid_update",
                "bid": bid,
                "remaining_time": remaining_time
            }
        )

    async def bid_update(self, event):
        bid = event["bid"]
        remaining_time = event["remaining_time"]

        await self.send(text_data=json.dumps({
            "bid": bid,
            "remaining_time": remaining_time
        }))
