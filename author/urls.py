from django.urls import path
from . import views

app_name = 'author'

urlpatterns = [
    path('dashboard', views.author_dashboard, name="author_dashboard"),
    path('content', views.author_content, name="author_content"),
    path('analytics', views.author_analytics, name="author_analytics"),
    path('community', views.author_community, name="author_community"),
    path('copyright', views.author_copyright, name="author_copyright"),
    path('earn', views.author_earn, name="author_earn"),
    path('content_details', views.content_details, name="content_details"),
    path('content_analytics', views.content_analytics, name="content_analytics"),
    path('content_comments', views.content_comments, name="content_comments"),
    path('content_translate', views.content_translate, name="content_translate"),
    path('content_copyright', views.content_copyright, name="content_copyright")
]