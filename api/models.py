from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Topic(models.Model):
    title = models.CharField(max_length=10, verbose_name='Название')
    body = models.CharField(max_length=100, verbose_name='Текст')
    number_of_comments = models.IntegerField(default=0, verbose_name='Кол-во комментриев')
    number_of_likes = models.IntegerField(default=0, verbose_name='Кол-во лайков')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()


class Comment(models.Model):
    body = models.CharField(max_length=100, verbose_name='Текст')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class TopicLike(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
