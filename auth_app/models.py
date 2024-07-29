from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
ROLE_CHOICE = [
    ('hotel', 'HOTEL'),
    ('user', 'USER'),
    ('admin', 'ADMIN'),
]

class Accounts(AbstractUser):
    full_name = models.CharField(max_length=100, null=False, blank=False)
    photo = models.ImageField(upload_to='profile_photos', default='images/profile.png')
    role = models.CharField(choices=ROLE_CHOICE, default='USER', max_length=100)
    
    def __Str__(self):
        return self.username