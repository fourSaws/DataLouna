from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, CategoryNode, Keywords, Keyword_Article
from .serializer import NodeSerializer


def RedirectToAdmin(request):
    return redirect('/admin/')


class getArticle(APIView):
    id_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[id_param_config])
    def get(self, request):
        param_id = self.request.query_params.get('id')
        try:
            instance = Article.objects.filter(id=param_id).values()[0]
            return Response(instance)
        except IndexError:
            return Response(
                {'getArticle_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST
            )


class getChildren(APIView):
    serializer_class = NodeSerializer
    parent_param_config = openapi.Parameter(
        'parent_id',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[parent_param_config])
    def get(self, request):
        parent_id = self.request.query_params.get('parent_id')
        queryset = CategoryNode.objects.filter(parent_id=parent_id)
        try:
            queryset[0]
        except IndexError:
            return Response(
                {'getChildren_Error': 'ID not found'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class getNode(APIView):
    serializer_class = NodeSerializer
    id_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[id_param_config])
    def get(self, request):
        id = self.request.query_params.get('id')
        queryset = CategoryNode.objects.filter(id=id)
        try:
            queryset[0]
        except IndexError:
            return Response(
                {'getNode_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class getArticlesByKeyWords(APIView):
    serializer_class = NodeSerializer
    word_param_config = openapi.Parameter(
        'word',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[word_param_config])
    def get(self, request):
        word = self.request.query_params.get('word')
        id_by_word = Keywords.objects.filter(text=word).values('id')[0]
        print(f"{id_by_word=}")
        keyword_A = Keyword_Article.objects.filter(keywords_id=id_by_word['id']).values(
            'article_id'
        )
        print(f"{keyword_A=}")
        print(len(keyword_A))
        article_array = []
        for i in range(len(keyword_A)):
            Articles = Article.objects.filter(id=keyword_A[i]['article_id']).values()[0]
            article_array.append(Articles)
        return Response(article_array)
