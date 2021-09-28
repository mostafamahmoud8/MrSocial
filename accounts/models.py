from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
def Uplaod_user_image(instance,filename):
     return 'Profile/picture/{username}/{filename}'.format(username=instance.username,filename=filename)

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user  = self.model(email=email,username=username ,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username ,password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, username ,password, **extra_fields)

    def create_superuser(self, email, username ,password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        return self._create_user(email, username ,password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'),unique=True
                               ,error_messages={
                                   'unique':_('A user with email aleardy exists.')}
                               )
    image = models.ImageField(upload_to=Uplaod_user_image)

    birth_date = models.DateField(_('Birth Date'),blank=True,null=True)

    slug = models.SlugField(allow_unicode=True,unique=False)


    friendship = models.ManyToManyField('self',blank=True,through='FriendShip',through_fields=('source','target'))
    block  = models.ManyToManyField('self',blank=True,through='Block',through_fields=('source','target'))

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username'] 

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse('accounts:profile',kwargs={'slug':self.slug})

    def save(self, *args,**kwargs):
        self.slug = slugify(self.username)
        super().save(*args,**kwargs)

class Block(models.Model):
    source = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='sourceblock')
    target = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='targetblock')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.source.username)+' has blocked '+str(self.target.username)

class FriendShip(models.Model):
    source = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='source')
    target = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='target')
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.source.username)+' friend request to '+str(self.target.username)