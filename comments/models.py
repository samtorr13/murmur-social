from django.db import models

from post.models import Post
from core.models import GlobalPID
from users.models import User


# Create your models here.

class Comment(models.Model):
    global_pid = models.OneToOneField(GlobalPID, on_delete=models.CASCADE, primary_key=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    co_content = models.TextField(max_length=500, null=False, blank=False, verbose_name="Comentario")
    anon = models.BooleanField(default=False)
    creat_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicacion")
    is_reply = models.BooleanField(default=False)

    class Meta:
        app_label = "post"

    def __str__(self):

        return f'comentario n° {self.global_pid}'

    def save(self, *args, **kwargs):
        if not self.global_pid_id:
            global_pid_obj = GlobalPID.objects.create()
            self.global_pid = global_pid_obj
        super().save(*args, **kwargs)
        if self.parent:
            self.is_reply = True