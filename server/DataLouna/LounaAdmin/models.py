from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    photo = models.ImageField(blank=True)

