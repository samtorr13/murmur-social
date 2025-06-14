from django.db import models

class GlobalPID(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.id)