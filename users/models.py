from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    favourite_book = models.CharField(default='', max_length=150)
    favourite_genre = models.CharField(default='', max_length=150)
    mobile_phone = PhoneNumberField(null=True, blank=True, unique=True)

    def __str__(self):
        return f'Profile username:{self.user.username} '
