from django.db import models
from groups.models import Group
from django.contrib.auth import get_user_model
import json
# Create your models here.

User = get_user_model()

def Uplaod_post_image(instance,filename):
    return 'posts/image/{username}/{id}/{filename}'.format(username=instance.owner.username,id=instance.id,filename=filename)

class Post(models.Model):
    content =  models.TextField(blank=True,null=True)
    image = models.ImageField(upload_to=Uplaod_post_image,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userposts')
    likes  = models.ManyToManyField(User,through='Like',through_fields=('post','user'),related_name='userlikes',blank=True)
    shares = models.ManyToManyField(User,through='Share',through_fields=('post','user'),related_name='usershares')
    comments = models.ManyToManyField(User,through='Comment',through_fields=('post','user'),related_name='usercomments')
    belong_to = models.ForeignKey(Group,on_delete=models.CASCADE,related_name='groupposts',null=True,blank=True)
    
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.content
    
    def serialize(self):
        if self.image:
            url = self.image.url
        else:
            url = ""
        context = {'content':self.content,'image':url}
        return json.dumps(context)
    
    def getComments(self):
        return Comment.objects.filter(post__id=self.id)
    def getLikes(self):
        return Like.objects.filter(post__id=self.id)
    def getShares(self):
        return Share.objects.filter(post__id=self.id)
    


    


class Like(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username  

class Share(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
    
