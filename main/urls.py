from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name="index"),
    path('trending', views.index, name="trending"),
    path('recent', views.index, name="recent"),
    path('popular', views.index, name="popular"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('book_view/<str:slug>', views.book_view, name="book_view"),
    path('newscast', views.news_cast, name="news_cast"),
    path('news/<int:news_id>', views.news, name="news"),
    path('search', views.search_results, name='search'),
    path('history', views.history, name='history'),
    path('continue-reading', views.continue_reading, name='continue_reading'),
    path('toggle_follow', views.toggle_follow, name="toggle_follow"),
    path('toggle_like', views.toggle_like, name="toggle_like"),
    path("submit-comment/", views.CommentView.as_view(), name="submit_comment"),
    path('delete-comment/<int:comment_id>', views.delete_comment, name="delete_comment"),
    path('subscriptions', views.subscriptions, name="subscriptions"),
    path('collections', views.collections, name="collections"),
    path('collection/<str:collection_name>', views.collection, name="collection"),
    path('add_to_collection/<str:slug>/<str:collection_name>', views.add_to_collection, name="add_to_collection"),
    path('remove_from_collection/<str:slug>/<str:collection_name>', views.remove_from_collection, name="remove_from_collection"),
    path('delete_collection/<int:collection_id>', views.delete_collection, name="delete_collection"),
    path('clear_notifications', views.clear_notifications, name="clear_notifications"),
    path('mark_all_as_read', views.mark_all_as_read, name="mark_all_as_read"),
    path('load-more-data', views.load_more_data, name="load_more_data"),
    path('temp', views.temp_book_view)
]