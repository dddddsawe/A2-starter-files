from django.urls import path
from .views import register, login_view, logout_view, ProfileView, ProfileUpdateView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/view/', ProfileView.as_view(), name='profile_view'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_update'),
]