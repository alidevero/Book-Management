from django.db import models
from django.db import models
from django.conf import settings
from Auth.models import *


class Friendship(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    )

    sender = models.ForeignKey(User, related_name="sent_requests", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_requests", on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")

    def accept(self):
        """Accept friend request"""
        self.status = "accepted"
        self.save()

    def reject(self):
        """Reject friend request"""
        self.status = "rejected"
        self.save()


# Create your models here.
