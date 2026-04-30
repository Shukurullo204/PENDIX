from django.urls import re_path
from . import consumers
# routing это вещь которое соединяет линию
# \w+ это узнаватель id чата
# и это всё передаем в ChatConsumer
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<thread_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]