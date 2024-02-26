from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('Boy', 'Boy'),
        ('Girl', 'Girl'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    user_lover = models.OneToOneField('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_lover_relation')
