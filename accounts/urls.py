from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', views.handleLogin, name='login'),
    path('register', views.handleSignup, name='register'),
    path('logout', views.logoutView, name="logout"),
    path('profile', views.profile, name="profile")
]