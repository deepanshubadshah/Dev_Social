from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.cache import cache
import datetime
from proj_social import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default= 'no_pic.png', upload_to='prof_pic')
    name = models.CharField(default= 'Users name', max_length = 150)

    def __self__(self):
        return '{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False

class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.CASCADE)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)
