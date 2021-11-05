from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from posts.models import Like,Share,Comment
from accounts.models import FriendShip
# Create your models here.

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserNotifcations')
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    status = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username


@receiver(post_save,sender=Comment)
@receiver(post_save,sender=Share)
@receiver(post_save,sender=Like)
@receiver(post_save,sender=FriendShip)
def notification_create_handler(sender, instance, created, **kwargs):
        
    if sender == Comment:
        if created:
            notification = Notification(user = instance.post.owner,sender = instance.user,content_object=instance)
            notification.save()

    elif sender == Like :
        if created:
            notification = Notification(user = instance.post.owner,sender = instance.user,content_object=instance)
            notification.save()

    elif sender == Share :
        if created:
            notification = Notification(user = instance.post.owner,sender = instance.user,content_object=instance)
            notification.save()

    elif sender == FriendShip :
        if created:
            notification = Notification(user = instance.target,sender = instance.source,content_object=instance)
            notification.save()
        else:
            notification = Notification(user = instance.source,sender = instance.target,content_object=instance)
            notification.save()
            
            

@receiver(post_delete,sender=Comment)
@receiver(post_delete,sender=Share)
@receiver(post_delete,sender=Like)
@receiver(post_delete,sender=FriendShip)
def notification_delete_handler(sender, instance,**kwargs):
        
    if sender == Comment:
        try:
             notification = Notification.objects.get(user = instance.post.owner,sender = instance.user,object_id=instance.id)
             notification.delete()
        except Notification.DoesNotExist as e:
            print(e)

    elif sender == Like :
        try:
            notification = Notification.objects.get(user = instance.post.owner,sender = instance.user,object_id=instance.id)
            notification.delete()
        except Notification.DoesNotExist as e:
            print(e)

    elif sender == Share :
        try:
            notification = Notification.objects.get(user = instance.post.owner,sender = instance.user,object_id=instance.id)
            notification.delete()
        except Notification.DoesNotExist as e:
            print(e)

    elif sender == FriendShip :
        try:
            notification = Notification.objects.get(user = instance.target,sender = instance.source,object_id=instance.id)
            notification.delete()
        except Notification.DoesNotExist as e:
            print(e)

