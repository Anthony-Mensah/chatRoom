from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='avatar.svg', upload_to='profile_pics', null=True)
    bio = models.CharField(max_length=500,default='',null=True,blank=True)
    name = models.CharField(max_length=50,default='',null=True)

    def __str__(self):
        return self.name
