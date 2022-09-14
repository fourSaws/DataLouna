from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Короткое описание')
    text = models.TextField(verbose_name='Текст статьи')
    photo = models.ImageField(blank=True, verbose_name='Фото')

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Статьи'
        verbose_name_plural = 'Статьи'


class Keywords(models.Model):
    text = models.CharField(max_length=64, verbose_name='Ключевые слова')

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = 'Ключевые слова'
        verbose_name_plural = 'Ключевые слова'


class Keyword_Article(models.Model):
    keywords_id = models.ForeignKey('Keywords',on_delete=models.CASCADE,verbose_name='ID Ключевого слова')
    article_id = models.ForeignKey('Article',on_delete=models.CASCADE,verbose_name='ID Статьи')

    def __str__(self):
        return "Ключевые слова"

    class Meta:
        verbose_name = 'Ключевые слова статей'
        verbose_name_plural = 'Ключевые слова статей'



class CategoryNode(models.Model):
    children = models.ForeignKey('CategoryNode',on_delete=models.CASCADE,related_name='Ребенок',blank=True,null=True)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('CategoryNode',on_delete=models.CASCADE,related_name='Родитель',blank=True,null=True)
    articles = models.ForeignKey('Article',on_delete=models.CASCADE,related_name='Статьи',blank=True,null=True)
    valid = models.BooleanField()


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Узел'
        verbose_name_plural = 'Узел'

