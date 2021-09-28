from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

# Create your models here.

User = get_user_model()

def Uplaod_group_image(instance,filename):
    return 'groups/image/{name}/{filename}'.format(name=instance.name,filename=filename)

class Group(models.Model):
    name = models.CharField(max_length=200,unique=True,error_messages={'unique':_('A group with that name aleardy exists.')})
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=Uplaod_group_image,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='mygroups')
    members = models.ManyToManyField(User,through='Membership',through_fields=('group','user'),related_name='usergroups')


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    

class Membership(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    join_date = models.DateTimeField(_('join date'),auto_now_add=True)

    def __str__(self) -> str:
        return self.group.name
    
    class Meta:
        verbose_name = 'Membership'
        verbose_name_plural = 'Memberships'



