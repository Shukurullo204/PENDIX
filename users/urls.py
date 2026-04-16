from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import smart_auth_view, ProfileDetailView, profile_edit

urlpatterns = [
    path('auth/smart/', smart_auth_view, name='smart_auth'),
    path('logout/', LogoutView.as_view(next_page='ad_list'), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', profile_edit, name='profile_edit'),
]