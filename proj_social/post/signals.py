from django.db.models.signals import post_save
from .models import Post, Notification
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(post=instance)

@receiver(post_save, sender=Post)
def save_notification(sender, instance, **kwargs):
    instance.notification.save()
