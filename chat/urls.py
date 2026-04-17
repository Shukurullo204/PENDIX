from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_list'),
    # Добавляем этот путь, чтобы ссылка /chat/5/ тоже работала
    path('<int:thread_id>/', views.chat_view, name='chat_detail'),
    path('start/<int:seller_id>/<int:ad_id>/', views.CreateOrGetChatView.as_view(), name='create_or_get_chat'),

]