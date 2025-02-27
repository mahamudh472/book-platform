from django.db import models
from django.contrib.auth.models import User

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def followers_count(self):
        return self.followers.count()
    
    def get_total_views(self):
        return self.user.books.aggregate(models.Sum('views'))['views__sum'] or 0