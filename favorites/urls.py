from django.urls import path
from . import views

app_name = 'favorites' # Пространство имен для удобства

urlpatterns = [
    path('', views.favorites_list, name='list'),
    path('toggle/<int:ad_id>/', views.toggle_favorite, name='toggle'),
]