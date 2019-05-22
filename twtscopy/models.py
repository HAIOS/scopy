from django.db import models
from django.utils import timezone


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    latitude  = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    range = models.IntegerField()
    time = models.DateTimeField(default=timezone.now)
    q = models.CharField(max_length=255,default="",blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name


class Tweets(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    searchKey = models.CharField(max_length=255,default="",blank=True)
    _json = models.TextField(default="{}")

    def __str__(self):
        return self.text

class HashTags(models.Model):
    id = models.IntegerField(primary_key=True)
    tweet = models.ForeignKey(Tweets, on_delete=models.CASCADE)
    hashtag = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.hashtag
