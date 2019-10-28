from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length = 150)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete= models.CASCADE)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    reply = models.ForeignKey('Comment', null=True, related_name="replies", on_delete= models.CASCADE)
    content = models.TextField(max_length=180)
    date_commented = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title, str(self.author.username))

class Notification(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __self__(self):
        return '{self.post.title} Notification'
