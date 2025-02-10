from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="index"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('book_view/<str:slug>', views.book_view, name="book_view"),
    path('newscast', views.news_cast, name="news_cast"),
    path('search', views.search_results, name='search'),
    path('toggle_follow', views.toggle_follow, name="toggle_follow"),
    path('toggle_like', views.toggle_like, name="toggle_like"),
    path("submit-comment/", views.CommentView.as_view(), name="submit_comment"),
    path('delete-comment/<int:comment_id>', views.delete_comment, name="delete_comment")
]