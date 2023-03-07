from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/view/', views.view_profile, name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
]
