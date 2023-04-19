from django.db import models 
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    favorite = models.ManyToManyField(to='tabi.Tabi', verbose_name='お気に入りの場所', blank=True)
    description = models.TextField(verbose_name='プロフィール', null=True, blank=True)
    
    
    class Meta:
        verbose_name_plural = 'CustomUser'