from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Activity(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='UserActivity')
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    action = models.CharField(max_length=150,blank=True,null=True)
    created_at =models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Activity Log'
        verbose_name_plural = 'Activities logs'

    def __str__(self):
        return self.user.username
    
