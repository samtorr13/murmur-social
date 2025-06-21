from django.db import models
from core.models import GlobalPID
from users.models import User


class Post(models.Model):
    global_pid = models.OneToOneField(GlobalPID, on_delete=models.CASCADE, primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default="1")
    po_content = models.TextField(max_length=500, null=False, blank=False,verbose_name="post")
    creat_date = models.DateTimeField(auto_now_add=True)
    anon = models.BooleanField(default=False)
    disabled = models.BooleanField(default=False)
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    def __str__(self):
        return f'Post n°{self.global_pid}'

    def save(self, *args, **kwargs):
        if not self.global_pid_id:
            global_pid_obj = GlobalPID.objects.create()
            self.global_pid = global_pid_obj
        super().save(*args, **kwargs)
