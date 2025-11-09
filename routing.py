from django.urls import re_path
from . import consumers

# Define as rotas do WebSocket que o asgi.py irá usar

websocket_urlpatterns = [
    # Rota para o chat de um evento específico
    # Ex: ws://localhost:8000/ws/chat/123/
    re_path(r'ws/chat/(?P<event_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]