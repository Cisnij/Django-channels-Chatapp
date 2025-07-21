from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile, AddFriend
from django.contrib.auth.models import User

#Taọ Profile tự động mỗi khi user mới được tạo
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objecs.create(user=instance,username=instance.username)