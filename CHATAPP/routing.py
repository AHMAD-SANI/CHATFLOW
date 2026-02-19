from django.urls import path
from CHATAPP.consumers import chat_consumer

websocket_urlpatterns = [
    path('ws/chats/<str:room_id>/', chat_consumer.as_asgi()),
]


