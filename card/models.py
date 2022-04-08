from django.db import models
from taggit.managers import TaggableManager
from user.models import User
# Create your models here.


class TimeStampedModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Gift(TimeStampedModel):
    class Meta:
        db_table = "gift"

    gift_name = models.CharField(max_length=200)
    gift_desc = models.TextField(blank=True)
    gift_img = models.ImageField(upload_to="gift/")
    tags = TaggableManager(blank=True)


class Message(TimeStampedModel):
    class Meta:
        db_table = "message"
    
    to_user = models.ForeignKey(User, related_name="to_user",on_delete=models.CASCADE)
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    msg = models.TextField(blank=True)
    deco = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=200, blank=True)
    top = models.IntegerField(default=0)
    left = models.IntegerField(default=0)
    read = models.BooleanField(default=False)


class Decoration(TimeStampedModel):
    class Meta:
        db_table = "decoration"

    deco_name = models.CharField(max_length=200)
    deco_img = models.ImageField(upload_to="deco/")
