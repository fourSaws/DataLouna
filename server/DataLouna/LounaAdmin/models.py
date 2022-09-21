from django.db import models


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='Короткое описание')
    text = models.TextField(verbose_name='Текст статьи')
    photo = models.ImageField(blank=True, verbose_name='Фото')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Keywords(models.Model):
    text = models.CharField(max_length=64, verbose_name='Ключевое слово')

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = 'Ключевые слова'
        verbose_name_plural = 'Ключевые слова'


class Keyword_Article(models.Model):
    keywords_id = models.ForeignKey(
        'Keywords',
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name='ID Ключевого слова',
        null=True #TODO: Delete this on the prod
    )
    article_id = models.ForeignKey(
        'Article', default=None, on_delete=models.SET_DEFAULT, verbose_name='ID Статьи', null=True
    )

    def __str__(self):
        return "Ключевые слова"

    class Meta:
        verbose_name = 'Ключевое слово статьи'
        verbose_name_plural = 'Ключевое слово статьи'


class CategoryNode(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'CategoryNode',
        on_delete=models.CASCADE,
        related_name='parent_rel',
        blank=True,
        null=True,
    )
    articles = models.ManyToManyField(
        'Article', related_name='art', blank=True,
    )
    valid = models.BooleanField()
    final = models.BooleanField(default=False)

    def articles_names(self):
        return ', '.join([a.title for a in self.articles.all()])

    articles_names.short_description = "articles"

    def get_id(self):
        return self.articles.values('id')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

