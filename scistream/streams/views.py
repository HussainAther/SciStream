from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Stream
from django.views.decorators.csrf import csrf_exempt
import json

class Stream(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(auto_now_add=True)
    is_live = models.BooleanField(default=False)

    def __str__(self):
        return self.title

@login_required
@csrf_exempt
def start_stream(request):
    if request.method == "POST":
        data = json.loads(request.body)
        stream = Stream.objects.create(
            user=request.user, title=data.get("title", "New Stream"), description=data.get("description", ""), is_live=True
        )
        return JsonResponse({"message": "Stream started", "stream_id": stream.id})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def stop_stream(request, stream_id):
    if request.method == "POST":
        stream = get_object_or_404(Stream, id=stream_id, user=request.user)
        stream.is_live = False
        stream.save()
        return JsonResponse({"message": "Stream stopped"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def list_streams(request):
    streams = Stream.objects.filter(is_live=True).values("id", "title", "description", "user__username")
    return JsonResponse({"streams": list(streams)})

from django.urls import path
from .views import start_stream, stop_stream, list_streams

urlpatterns = [
    path("start/", start_stream, name="start_stream"),
    path("stop/<int:stream_id>/", stop_stream, name="stop_stream"),
    path("list/", list_streams, name="list_streams"),
]

# Django Channels for WebSockets
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "chat_global"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        username = self.scope["user"].username

        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "username": username}
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        await self.send(text_data=json.dumps({"message": message, "username": username}))
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Stream
from django.contrib.auth.decorators import login_required

@login_required
def start_stream(request):
    stream = Stream.objects.create(user=request.user, is_live=True, title="New Stream")
    return JsonResponse({"message": "Stream started", "stream_id": stream.id})

@login_required
def stop_stream(request, stream_id):
    stream = get_object_or_404(Stream, id=stream_id, user=request.user)
    stream.is_live = False
    stream.save()
    return JsonResponse({"message": "Stream stopped"})

