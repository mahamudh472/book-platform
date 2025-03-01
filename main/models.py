from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField
from  django.utils import timezone
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    
    def __str__(self):
        return self.name

class PublicBookManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(status="Private")

class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField()
    content = CKEditor5Field(config_name="extends") 
    language = models.CharField(max_length=50, default="default")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_books', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_books', blank=True)
    views = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    status = models.CharField(max_length=50, default='Public')

    objects = models.Manager()
    public_objects = PublicBookManager()

    def __str__(self):
        return self.title
    
    def likes_count(self):
        return self.likes.count()
    
    def dislikes_count(self):
        return self.dislikes.count()
    

class BookView(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_views")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class News(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    description = models.TextField()
    content = CKEditor5Field(config_name="extends") 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_news', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_news', blank=True)
    views = models.PositiveIntegerField(default=0)

class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='news_images/')

    def __str__(self):
        return f"Image for {self.news.title}"

class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_comment", blank=True)
    dislikes = models.ManyToManyField(User, related_name="disliked_comment", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # e.g., 1-5
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_list')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_book_ids(self):
        return list(self.reading_list.values_list('book_id', flat=True))

class ReadingList(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    target_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Report(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    books = models.ManyToManyField(Book, related_name='tags', blank=True)

    def __str__(self):
        return self.name

class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="book_history", blank=True, null=True)
    news = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="news_history", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField()

class AudioBook(models.Model):
    book = models.ForeignKey(Book, related_name='audiobooks', on_delete=models.CASCADE)
    language = models.CharField(max_length=50)
    narrator = models.CharField(max_length=255, blank=True, null=True)
    file = models.FileField(upload_to='audiobooks/')

class Booktranslation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='translations')
    language = models.CharField(max_length=50)
    translated_title = models.CharField(max_length=255)
    translated_description = models.TextField()
    translated_content = CKEditor5Field(config_name='default')