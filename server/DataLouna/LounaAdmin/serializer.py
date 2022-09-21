from rest_framework import serializers
from .models import *


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


class NodeSerializerUnpack(serializers.ModelSerializer):
    class Meta:
        model = CategoryNode
        fields = ('id', 'name')


class NodeSerializer(serializers.ModelSerializer):
    articles = ArticleSerializer(read_only=True, many=True)

    class Meta:
        model = CategoryNode
        fields = ('id', 'name', 'parent', 'articles', 'final')


class NodeSerializerArticleId(serializers.ModelSerializer):
    class Meta:
        model = CategoryNode
        fields = ('id', 'name', 'parent', 'final')
