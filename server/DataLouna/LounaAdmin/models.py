from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


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
        null=True,
    )
    article_id = models.ForeignKey(
        'Article',
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name='ID Статьи',
        null=True,
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
        'Article',
        related_name='art',
        blank=True,
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

    def save(self, *args, **kwargs):
        super(CategoryNode, self).save()
        for p in CategoryNode.objects.all().values('parent'):
            if self.parent.id == p['parent'] and self.articles.all() != None:
                self.valid = True
                return super(CategoryNode, self).save()
            else:
                self.valid = False
                return super(CategoryNode, self).save()

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


@receiver(m2m_changed, sender=CategoryNode.articles.through)
def children_post_save(instance: CategoryNode, action, *args, **kwargs):
    if action != 'post_add' and action != 'post_remove':
        return None
    for p in CategoryNode.objects.all().values('parent'):
        if instance.parent.id == p['parent'] and instance.articles.all() != None:
            instance.valid = True
            instance.save()
        else:
            instance.valid = False
            instance.save()
