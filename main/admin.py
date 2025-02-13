from django.contrib import admin
from .models import Book, Category,Collection,Comment,Notification,Rating,ReadingList,Report,Tag, News, NewsImage, History
# Register your models here.

admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Comment)
admin.site.register(Notification)
admin.site.register(Rating)
admin.site.register(ReadingList)
admin.site.register(Report)
admin.site.register(Tag)
admin.site.register(History)


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [NewsImageInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'likes_count', 'dislikes_count', 'views']