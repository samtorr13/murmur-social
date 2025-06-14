from django.db import models
from django.contrib.auth.models import User
from murmur.settings import AUTH_USER_MODEL as user

class Community(models.Model):
    name = models.CharField(max_length=100, unique=True)

    description = models.TextField(blank=True)
    createdat = models.DateTimeField(auto_now_add=True)
    createdBy = models.ForeignKey(user, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='comm_images/', blank=True)

    class Meta:
        verbose_name_plural = 'Communities'

    def __str__(self):
        return self.name