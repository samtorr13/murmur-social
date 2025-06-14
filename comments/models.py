from django.db import models

from post.models import Post
from core.models import GlobalUID
from users.models import User


# Create your models here.

class Comment(models.Model):
    global_uid = models.OneToOneField(GlobalUID, on_delete=models.CASCADE, blank=True, null=True)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    co_content = models.TextField(max_length=500, null=False, blank=False, verbose_name="Comentario")
    anon = models.BooleanField(default=False)
    creat_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de publicacion")

    class Meta:
        app_label = "post"

    def __str__(self):
        resumen = self.co_content[:30] + ("..." if len(self.co_content) > 30 else "")

        return f'post {self.id} by UID {self.author}: {resumen}'

    def save(self, *args, **kwargs):
        if not self.global_uid:
            global_uid_obj = GlobalUID.objects.create()
            self.global_uid = global_uid_obj
        super().save(*args, **kwargs)