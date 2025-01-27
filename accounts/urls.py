from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name="logout"),
    path('profile', views.profile, name="profile")
]