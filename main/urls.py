from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="index"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('book_view/<str:slug>', views.book_view, name="book_view"),

]