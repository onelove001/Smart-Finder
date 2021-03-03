from django.db import models
from django.urls import reverse
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from core.models import customUser
from chat.timesin import calcEpochSec, timesince
import datetime




class ThreadManager(models.Manager):

    def get_all_users(self, sender):
        qs = customUser.objects.all().exclude(username = sender)
        return qs

    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): #get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    timestamp2   = models.DateTimeField(default=timezone.now)
    
    objects      = ThreadManager()

    def __str__(self):
        return f"{self.first.username} to {self.second.username}"

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def get_last_message(self):
        messages = []
        for chat in self.chatmessage_set.all():
            messages.append(chat.message)
        return str(messages[-1:]).strip("['']")

    def get_time_message(self):
        time = []
        for chat in self.chatmessage_set.all():
            t = (calcEpochSec(datetime.datetime.now()) - calcEpochSec(chat.timestamp2))
            if t < 3600:
                a = int(t/60)
                z = (str(a) + " minutes ago").strip("-")
                time.append(z)

            elif t > 3600:
                a = int(t/60/60)
                z = (str(a) + " hours ago").strip("-")
                time.append(z)

        return str(time[-1:]).strip("['']")


    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    timestamp2 = models.DateTimeField(default = timezone.now)

    