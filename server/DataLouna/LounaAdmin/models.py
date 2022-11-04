import os
from datetime import datetime
from uuid import uuid4

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import m2m_changed, pre_delete
from django.dispatch import receiver


class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        _, ext = os.path.splitext(name)
        return uuid4().hex + ext


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="Короткое описание")
    text = models.TextField(verbose_name="Текст статьи")
    photo = models.ImageField(blank=True, upload_to='someimages', storage=UUIDFileStorage(), verbose_name="Фото")
    links = models.ManyToManyField(to="Article", verbose_name="Ссылки на статьи",blank=True, null=True)
    on_top = models.BooleanField(default=False, verbose_name="Верхняя статья")

    def links_many_to_many(self):
        return ', '.join([a.title for a in self.links.all()])

    links_many_to_many.short_description = "Ссылка на статьи"

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


class User(models.Model):
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
