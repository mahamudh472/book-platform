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
    path('book-details/<str:slug>', views.content_details, name="content_details"),
    path('book-analytics/<str:slug>', views.content_analytics, name="content_analytics"),
    path('book-comments/<str:slug>', views.content_comments, name="content_comments"),
    path('book-translate/<str:slug>', views.content_translate, name="content_translate"),
    path('book-audio/<str:slug>', views.content_audio, name="content_audio"),
    path('book-copyright/<str:slug>', views.content_copyright, name="content_copyright"),
    path('write-book', views.write_book, name="write_book"),
    path('create-news', views.create_news, name="create_news"),
    path('get-translation/<int:book_id>/<int:translation_id>', views.get_translation, name='get_translation')

]