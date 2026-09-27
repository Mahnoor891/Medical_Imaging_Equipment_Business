from django.db import models
from django.contrib.auth.models import User

class Hospital(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    branch = models.CharField(max_length=200, blank= True, default='Main')
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.branch}"