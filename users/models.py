from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission


# Create your models here.

class User(AbstractUser):
    username = models.CharField(verbose_name='Nombre de usuario', max_length=100, unique=True)
    bio = models.TextField(verbose_name='Bio', blank=True)
    avatar = models.ImageField(verbose_name='Imagen', upload_to='avatars', blank=True)

    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('editor', 'Editor'),
    )

    role = models.CharField(verbose_name='Tipo', max_length=6, choices=ROLE_CHOICES, default='admin')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == "admin":
            self.is_staff = True
            self.is_superuser = True
        elif self.role == "editor":
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs)

        if self.role != "editor":
            self.user_permissions.clear()
            return

        modelos_a_permitir = ['post', 'comment', 'report']

        for modelo in modelos_a_permitir:
            try:
                content_type = ContentType.objects.get(app_label='post', model=modelo)
                perms = Permission.objects.filter(
                    content_type=content_type,
                    codename__in=[f'change_{modelo}', f'view_{modelo}', f'delete_{modelo}', f'add_{modelo}']
                    )
                for perm in perms:
                    self.user_permissions.add(perm)
            except ContentType.DoesNotExist:
                continue

