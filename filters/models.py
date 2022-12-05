from django.db import models
from django.conf import settings
from accounts.models import User


class Categories(models.Model):
    title = models.CharField(max_length=32)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=32, verbose_name="태그명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.name


class TestSet(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_articles')
    image = models.CharField(max_length=24, null=True)
    feature = models.CharField(max_length=150, null=True, blank=True)
    tag = models.ManyToManyField(Tag, verbose_name=Tag)

    def __str__(self):
        return self.title


class Comments(models.Model):
    article = models.ForeignKey(TestSet, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body


class PostImage(models.Model):
    post = models.ForeignKey(TestSet, on_delete=models.CASCADE, null=True)
    temp = models.CharField(max_length=36, null=True)
    image = models.ImageField(upload_to="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order = models.IntegerField(null=True)
