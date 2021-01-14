from django.db import models
from core.models import customUser
from django.utils import timezone



class Message(models.Model):
    sender = models.ForeignKey(customUser, on_delete = models.CASCADE, related_name = 'sender', null = True)
    receiver = models.ForeignKey(customUser, on_delete = models.CASCADE, related_name = 'receiver', null = True)
    content = models.TextField()
    time_stamp = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"{self.sender.username} messaged {self.receiver.username}"
   
    def get_last_10_messages(self):
        pass
        # return self.messages.objects.order_by('-time_stamp').all()[:10]