from django.urls import path
from .views import ReviewCreateView

urlpatterns = [
    path('add/<int:seller_id>/', ReviewCreateView.as_view(), name='review_add'),
]
