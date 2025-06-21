from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from comments.models import Comment
from post.models import Post
from users.models import User


# Create your models here.

class Report(models.Model):
    global_pid = models.IntegerField(null= False)

    # ContentType magic
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content = GenericForeignKey('content_type', 'object_id')

    reason = models.TextField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('reviewed', 'Revisado'),
        ('dismissed', 'Descartado'),
        ('removed', 'Contenido Eliminado'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    moderator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name="moderated_reports")
    review_notes = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'post'

    def __str__(self):
        return f'{self.content} - {self.reason} - by: {self.reporter}'

    def save(self, *args, **kwargs):
        if not self.content:
            # Detecta si el global_pid es de un Post o un Comment
            post = Post.objects.filter(global_pid=self.global_pid).first()
            comment = Comment.objects.filter(global_pid=self.global_pid).first()

            if post:
                self.content = post
            elif comment:
                self.content = comment
            else:
                raise ValueError("El GlobalPID no pertenece a ningún contenido conocido.")

        super().save(*args, **kwargs)