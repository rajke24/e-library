from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    favourite_book = models.CharField(default='', max_length=150)
    favourite_genre = models.CharField(default='', max_length=150)
    mobile_phone = models.CharField(default='', max_length=9)

    def __str__(self):
        return f'Profile username:{self.user.username} '
