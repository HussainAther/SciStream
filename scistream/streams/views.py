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

