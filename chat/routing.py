# chat/routing.py
from django.conf.urls import url
from chat.consumers import *

websocket_urlpatterns = [
    url(r"^messages/(?P<username>[\w.@+-]+$", chatConsumer),
]