from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserNotifcations')
    message = models.TextField(blank=True,default='notification message')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    status = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
