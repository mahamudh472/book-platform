from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Collection


@receiver(post_save, sender=User)
def create_default_collection(sender, instance, created, **kwargs):
    if created:
        Collection.objects.create(
            user=instance,
            name="My collection"
            )