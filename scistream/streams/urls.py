from django.urls import path
from .views import (
    start_stream,
    stop_stream,
    list_streams,
    get_stream_key,
    regenerate_stream_key,
)

urlpatterns = [
    path("start/", start_stream, name="start_stream"),
    path("stop/<int:stream_id>/", stop_stream, name="stop_stream"),
    path("list/", list_streams, name="list_streams"),
    path("stream/key/", get_stream_key, name="get_stream_key"),
    path("stream/key/regenerate/", regenerate_stream_key, name="regenerate_stream_key"),
]

