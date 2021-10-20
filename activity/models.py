from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from user_agents import parse

from posts.models import Post,Share,Like,Comment
from groups.models import Group,Membership

# Create your models here.

User = get_user_model()

class Activity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserActivity')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    action = models.CharField(max_length=150,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activities logs'

    def __str__(self):
        return self.user.username

class AuthActivityLog(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserAuthActivity')
    ipaddress = models.GenericIPAddressField(null=True)
    action = models.CharField(max_length=150,blank=True,null=True)
    browser = models.CharField(max_length=150,blank=True,null=True)
    os = models.CharField(max_length=150,blank=True,null=True)
    device = models.CharField(max_length=150,blank=True,null=True)
    is_mobile = models.BooleanField(default=False)
    is_tablet = models.BooleanField(default=False)
    is_pc = models.BooleanField(default=False)
    is_touch_capable = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    logtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Activity Auth Log'
        verbose_name_plural = 'Activities Auth logs'

    def __str__(self):
        return self.user.username


@receiver(post_save,sender=Post)
@receiver(post_save,sender=Group)
@receiver(post_save,sender=Comment)
@receiver(post_save,sender=Share)
@receiver(post_save,sender=Like)
@receiver(post_save,sender=Membership)
def activty_create_handler(sender, instance, created, **kwargs):
    if sender == Post :
        if created:
            activity = Activity(user=instance.owner,content_object=instance,action='created')
            activity.save()
        else:
            activity = Activity(user=instance.owner,content_object=instance,action='updated')
            activity.save()

    elif sender == Group :
        if created:
            activity = Activity(user=instance.owner,content_object=instance,action='created')
            activity.save()
        else:
            activity = Activity(user=instance.owner,content_object=instance,action='updated')
            activity.save()        

    elif sender == Comment:
        if created:
            activity = Activity(user=instance.user,content_object=instance,action='created')
            activity.save()
        else:
            activity = Activity(user=instance.user,content_object=instance,action='updated')
            activity.save()

    elif sender == Like :
        if created:
            activity = Activity(user=instance.user,content_object=instance,action='like')
            activity.save()

    elif sender == Share :
        if created:
            activity = Activity(user=instance.user,content_object=instance,action='share')
            activity.save()

    elif sender == Membership :
        if created:
            activity = Activity(user=instance.user,content_object=instance,action='join')
            activity.save()


    
@receiver(post_delete,sender=Post)
@receiver(post_delete,sender=Group)
@receiver(post_delete,sender=Comment)
@receiver(post_delete,sender=Share)
@receiver(post_delete,sender=Like)
@receiver(post_delete,sender=Membership)
def activty_delete_handler(sender, instance, **kwargs):
    if sender == Post :
        activity = Activity.objects.filter(user__id=instance.owner.id,object_id=instance.id)
        activity.delete()

    elif sender == Group :
        activity = Activity.objects.filter(user__id=instance.owner.id,object_id=instance.id)
        activity.delete()       

    elif sender == Comment:
        activity = Activity.objects.filter(user__id=instance.user.id,object_id=instance.id)
        activity.delete()

    elif sender == Like :
        activity = Activity.objects.filter(user__id=instance.user.id,object_id=instance.id)
        activity.delete()

    elif sender == Share :
        activity = Activity.objects.filter(user__id=instance.user.id,object_id=instance.id)
        activity.delete()

    elif sender == Membership :
        activity = Activity.objects.filter(user__id=instance.user.id,object_id=instance.id)
        activity.delete()

@receiver(user_logged_in,sender=User)
def activity_user_login(sender, request,user, **kwargs):
    print(request.META.get('REMOTE_ADDR'))
    ua_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(ua_string)

    activity = AuthActivityLog(user=user, ipaddress=request.META.get('REMOTE_ADDR'), action='log in',
                                browser=user_agent.browser.family, os=user_agent.os.family
                                ,device=user_agent.device.family, is_mobile=user_agent.is_mobile
                                ,is_tablet=user_agent.is_tablet, is_pc=user_agent.is_pc
                                ,is_touch_capable=user_agent.is_touch_capable, is_bot=user_agent.is_bot)

    activity.save()

@receiver(user_logged_out,sender=User)
def activity_user_logout(sender, request, user, **kwargs):
    print(request.META.get('REMOTE_ADDR'))
    ua_string = request.META.get('HTTP_USER_AGENT')
    user_agent = parse(ua_string)

    activity = AuthActivityLog(user=user, ipaddress=request.META.get('REMOTE_ADDR'), action='log out',
                               browser=user_agent.browser.family, os=user_agent.os.family,
                               device=user_agent.device.family, is_mobile=user_agent.is_mobile
                              ,is_tablet=user_agent.is_tablet ,is_pc=user_agent.is_pc 
                              ,is_touch_capable=user_agent.is_touch_capable ,is_bot=user_agent.is_bot)

    activity.save()  

        
