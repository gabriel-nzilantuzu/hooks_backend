from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('logger', consumers.HookConsumer.as_asgi())
]
