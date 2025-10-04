from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    following = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username
