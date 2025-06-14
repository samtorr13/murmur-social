from django.db import models


class Post(models.Model):
    author_uid =models.PositiveIntegerField()
    po_content = models.TextField()
    creat_date = models.DateTimeField(auto_now_add=True)
    anon = models.BooleanField(default=False)
    community = models.ForeignKey(
        'communities.Community',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    def __str__(self):
        resumen = self.po_content[:30] + ("..." if len(self.po_content) > 30 else "")

        return f'post {self.id} by UID {self.author_uid}: {resumen}'