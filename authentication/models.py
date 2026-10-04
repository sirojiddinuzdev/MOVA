from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # We can add custom fields here if needed
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
