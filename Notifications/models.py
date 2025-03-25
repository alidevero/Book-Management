from django.db import models

#Project Imports
from Auth.models import *
# Create your models here.

class NotificationModel(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"Notification for {self.user.email}:{self.message}"

