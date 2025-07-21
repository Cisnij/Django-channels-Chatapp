from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    pic = models.ImageField(blank=True,null=True)
    friends=models.ManyToManyField('Friend',related_name="friend",blank=True) #1 profile co nhieu ban be
    def __str__(self):
        return self.name

class Friend(models.Model):
    profile =models.OneToOneField(Profile, on_delete=models.CASCADE) #ban be chi co 1 profile
    def __str__(self):
        return self.profile.name

class Message(models.Model):
    mess= models.TextField()
    sender= models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE,related_name="receiver")
    seen=models.BooleanField(default=False)
    def __str__(self):
        return self.mess
    
class AddFriend(models.Model):
    sender_request=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="sender_request")
    receiver_request=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name="receiver_request")
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.sender_request.name