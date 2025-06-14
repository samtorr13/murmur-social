from django.db import models
from django.contrib.auth.models import AbstractUser
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

    role = models.CharField(verbose_name='Tipo', max_length=6, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == "admin":
            self.is_staff = True
            self.is_superuser = True
        elif self.role == "editor":
            self.is_staff = True
            self.is_superuser = False
            self.assign_mod_permissions()
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)

    def assign_mod_permissions(self):
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from post.models import Post, Comment

        post_perms = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Post))
        comment_perms = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Comment))

        self.user_permissions.set(list(post_perms) + list(comment_perms))