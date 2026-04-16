from django.urls import path
from .views import FavoriteToggleView

urlpatterns = [
    path('toggle/<int:ad_id>/', FavoriteToggleView.as_view(), name='favorite_toggle'),
]
