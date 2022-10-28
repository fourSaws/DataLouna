from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ("id", "title")


class UserSerializer(serializers.ModelSerializer):
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

    site_id = serializers.IntegerField()
    chat_id = serializers.IntegerField()
    subscription_status = serializers.CharField(max_length=255)
    subscription_paid_date = serializers.DateField()
    subscription_end_date = serializers.DateField()

    class Meta:
        model = User
        fields = "__all__"


class TopSerializer(serializers.ModelSerializer):
    links = ArticleSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields = ("id", "title", "text", "photo", "links", "on_top")
