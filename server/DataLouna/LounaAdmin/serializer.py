from rest_framework import serializers
from .models import *


class NodeSerializerUnpack(serializers.ModelSerializer):
    class Meta:
        model = CategoryNode
        fields = ('id','name')


class NodeSerializer(serializers.ModelSerializer):
    #children = NodeSerializerUnpack(read_only=True,many=True)
    class Meta:
        model = CategoryNode
        fields = ('id','name','parent','articles')
