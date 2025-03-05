from django.db import models
from django.contrib.auth.models import User
from main.models import Book
# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def get_total_views(self):
        return self.user.books.aggregate(models.Sum('views'))['views__sum'] or 0
    
class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_users")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers_users")
    followed_at = models.DateTimeField(auto_now_add=True)
    from_book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True, related_name="followed_from_book")

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate follows

    def __str__(self):
        return f"{self.follower} follows {self.following}"
