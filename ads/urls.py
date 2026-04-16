from django.urls import path

from .views import AdCreateView, AdDetailView, AdListView, AdUpdateView, UserAdListView

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('ad/create/', AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/', AdDetailView.as_view(), name='ad_detail'),
    path('ad/<int:pk>/edit/', AdUpdateView.as_view(), name='ad_edit'),
    path('user/<int:user_id>/ads/', UserAdListView.as_view(), name='user_ads'),
]