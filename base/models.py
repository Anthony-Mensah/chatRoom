from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# TOPIC
class Topic(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

# ROOM
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)#null=True means it can be blank
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)#blank=True means when we submit a form it can be blank
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created','-updated']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created','-updated']

    def __str__(self):
        return self.body[0:20]
