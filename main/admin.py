from django.contrib import admin
from .models import Book, Category,Collection,Comment,Notification,Rating,ReadingList,Report,Tag
# Register your models here.

admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(ReadingList)
admin.site.register(Report)
admin.site.register(Tag)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'likes_count', 'dislikes_count', 'views']