from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = "__all__"


class NodeSerializerUnpack(serializers.ModelSerializer):
    class Meta:
        model = CategoryNode
        fields = ("id", "name")


class NodeSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(read_only=True, many=True)

    class Meta:
        model = CategoryNode
        fields = ("id", "name", "parent", "articles", "final")


class NodeSerializerArticleId(serializers.ModelSerializer):
    class Meta:
        model = CategoryNode
        fields = ("id", "name", "parent", "final", "valid")


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
        model = modelUser
        fields = "__all__"
