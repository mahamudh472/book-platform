from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field
from autoslug import AutoSlugField

class Book(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title')
    description = models.TextField()
    content = CKEditor5Field(config_name="extends") 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_books', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_books', blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def likes_count(self):
        return self.likes.count()
    
    def dislikes_count(self):
        return self.dislikes.count()


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    books = models.ManyToManyField(Book, related_name='categories', blank=True)
    
    def __str__(self):
        return self.name


class Comment(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
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

class ReadingList(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='reading_list')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
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

