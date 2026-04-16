from django.urls import path
from .views import ThreadListView, ChatDetailView, CreateOrGetChatView

urlpatterns = [
    path('chat/', ThreadListView.as_view(), name='chat_list'),
    path('chat/<int:pk>/', ChatDetailView.as_view(), name='chat_detail'),
    path('chat/start/<int:seller_id>/<int:ad_id>/', CreateOrGetChatView.as_view(), name='create_or_get_chat'),
]