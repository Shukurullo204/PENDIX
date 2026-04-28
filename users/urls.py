from django.urls import path

from django.contrib.auth.views import LogoutView

from . import views                                               



urlpatterns = [

                                                              

    path('auth/smart/', views.smart_auth_view, name='smart_auth'),

    path('logout/', LogoutView.as_view(next_page='ad_list'), name='logout'),

    path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile_detail'),

    path('profile/edit/', views.profile_edit, name='profile_edit'),

    path('profile/', views.ProfileDetailView.as_view(), name='profile_me'),

]
