from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from accounts.models import CustomUser

# Create your models here.
class Tabi(models.Model):
    title = models.CharField('タイトル(32文字まで)',max_length=32)
    text = models.TextField('この旅の簡単な説明文、目標など') #説明文
    money = models.TextField('一人当たりの費用')
    date = models.CharField('日数 (例)二泊三日、日帰り...',max_length=8) #二泊三日とか
    thumbnail = models.ImageField('サムネイル写真',null=True, blank=True)
    tags = TaggableManager(blank=True)
    created_at = models.DateTimeField('作成日',auto_now_add=True)
    daylooked = models.IntegerField(default=0)
    weeklylooked = models.IntegerField(default=0)
    looked = models.PositiveIntegerField(default=0)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='related_post', blank=True)
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,verbose_name='投稿者')
    

    
    def __str__(self):
        return self.title
    
    
class TabiDate(models.Model):
    day = models.PositiveIntegerField('何日目か(日付が変わった時のみ入力)',blank=True) #1日目の1
    time = models.CharField('時間 (例)9:00',max_length=8) # 9:00
    move = models.TextField('その時間の説明 (例)清水寺を訪問、拝観料400円、滞在時間1時間、見所...')
    img = models.ImageField('スポットの写真(なくても可)',null=True, blank=True)
    target = models.ForeignKey(
        Tabi, verbose_name='紐ずく旅',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    def __str__(self):
        return self.time
    
    
class Comment(models.Model):
    text = models.TextField('本文')
    target = models.ForeignKey(Tabi, on_delete=models.PROTECT, verbose_name='どの記事へのコメントか')

    def __str__(self):
        return self.text[:20]
    
    
class Connection(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    following = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)
    
    def __str__(self):
           return self.user.username
    
    

    

    
    