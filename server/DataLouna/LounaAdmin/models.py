from datetime import datetime

from django.db import models
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Короткое описание")
    text = models.TextField(verbose_name="Текст статьи")
    photo = models.ImageField(blank=True, verbose_name="Фото")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class Keywords(models.Model):
    text = models.CharField(max_length=64, verbose_name="Ключевое слово")

    def __str__(self):
        return f"{self.text}"

    class Meta:
        verbose_name = "Ключевые слова"
        verbose_name_plural = "Ключевые слова"


class KeywordArticle(models.Model):
    keywords_id = models.ForeignKey(
        "Keywords",
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name="ID Ключевого слова",
        null=True,
    )
    article_id = models.ForeignKey(
        "Article",
        default=None,
        on_delete=models.SET_DEFAULT,
        verbose_name="ID Статьи",
        null=True,
    )

    def __str__(self):
        return "Ключевые слова"

    class Meta:
        verbose_name = "Ключевое слово статьи"
        verbose_name_plural = "Ключевое слово статьи"


class CategoryNode(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        "CategoryNode",
        on_delete=models.CASCADE,
        related_name="parent_rel",
        blank=True,
        null=True,
    )
    articles = models.ManyToManyField(
        "Article",
        related_name="art",
        blank=True,
    )
    valid = models.BooleanField(default=False)
    final = models.BooleanField(default=False)

    def articles_names(self):
        return ", ".join([a.title for a in self.articles.all()])

    articles_names.short_description = "articles"

    def get_id(self):
        return self.articles.values("id")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        print(f"save:{self}")
        if kwargs.get("super"):
            return super(CategoryNode, self).save()
        super(CategoryNode, self).save()
        has_kids = False
        for p in CategoryNode.objects.filter(parent=self.id):
            if p.valid and p != kwargs.get("deleted_child"):
                has_kids = True
                break
        has_articles = bool(self.articles.all())
        self.valid = has_kids != has_articles
        self.final = has_articles
        super(CategoryNode, self).save()
        if self.parent:
            self.parent.save()
        return super(CategoryNode, self).save()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class modelUser(models.Model):
    ZERO = "ZERO"
    FIRST = "FIRST"
    SECOND = "SECOND"
    THIRD = "THIRD"
    FOURTH = "FOURTH"
    STATUS_CHOICES = [
        (ZERO, "Нет аккаунта на сайте"),
        (FIRST, "Не оформил триал"),
        (SECOND, "Триал оформлен"),
        (THIRD, "Оформил (продлил?) подписку"),
        (FOURTH, "Карта удалена сразу"),
    ]

    site_id = models.IntegerField(verbose_name="ID на сайте", blank=True, null=True)
    chat_id = models.IntegerField(verbose_name="Чат ID", blank=True, null=True)
    subscription_status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=255,
        verbose_name="Статус подписки",
        null=True,
    )
    subscription_end_date = models.DateTimeField(verbose_name="Дата окончания подписки", null=True, blank=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.chat_id}"


@receiver(pre_delete, sender=CategoryNode)
def delete_image_hook(sender, instance: CategoryNode, using, **kwargs):
    instance.parent.save(deleted_child=instance)


@receiver(m2m_changed, sender=CategoryNode.articles.through)
def children_post_save(instance: CategoryNode, action, *args, **kwargs):
    print(f"m2m_changed:{instance}")
    if action != "post_add" and action != "post_remove":
        return None
    has_kids = False
    for p in CategoryNode.objects.filter(parent=instance.id):
        if p.valid:
            has_kids = True
            break

    has_articles = bool(instance.articles.all())
    instance.valid = has_kids != has_articles
    instance.final = has_articles
    instance.save(super=True)

    if instance.parent:
        instance.parent.save()
    print(f"m2m_changed:{has_kids=},{has_articles=}")
    return None

class NoviceNewsTellers(models.Model):
    after_time = models.DurationField(verbose_name="Переодичность рассылки")
    text = models.CharField(max_length=500, verbose_name="Текст")

    class Meta:
        verbose_name = "Рассылка новичку"
        verbose_name_plural = "Рассылку новичку"

    def __str__(self):
        return f"{self.after_time}"


class InactiveNewsTellers(models.Model):
    after_time = models.DurationField(verbose_name="Переодичность рассылки")
    text = models.CharField(max_length=500, verbose_name="Текст")

    class Meta:
        verbose_name = 'Рассылки "спящему" клиенту'
        verbose_name_plural = 'Рассылки "спящим" клиентам'

    def __str__(self):
        return f"{self.after_time}"


class Notification(models.Model):
    SUCCSESSFUL_PAYMENT = "SUCCSESSFUL_PAYMENT"
    UNSUCCESSFUL_PAYMENT = "UNSUCCESSFUL_PAYMENT"
    STATUS_CHOICES = [
        (SUCCSESSFUL_PAYMENT, "SUCCSESSFUL_PAYMENT"),
        (UNSUCCESSFUL_PAYMENT, "UNSUCCESSFUL_PAYMENT"),
    ]

    type = models.CharField(max_length=500, choices=STATUS_CHOICES)
    text = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Уведомление об оплате"
        verbose_name_plural = "Уведомления об оплате"

    def __str__(self):
        return f"{self.type}"

