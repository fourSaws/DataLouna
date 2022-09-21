from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, CategoryNode, Keywords, Keyword_Article
from .serializer import NodeSerializer, ArticleSerializer, NodeSerializerArticleId


def RedirectToAdmin(request):
    return redirect('/admin/')


class getArticle(APIView):
    id_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[id_param_config])
    def get(self, request):
        try:
            param_id = self.request.query_params.get('id')
        except ValueError:
            return Response({'ValueError'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Article.objects.filter(id=param_id).values()[0]
            return Response(instance)
        except IndexError:
            return Response(
                {'getArticle_Error': 'ID not found'}, status=status.HTTP_404_NOT_FOUND
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

        serializers = NodeSerializerArticleId(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class getNode(APIView):
    serializer_class = NodeSerializer
    id_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[id_param_config])
    def get(self, request):
        id = self.request.query_params.get('id')
        if id:
            queryset = CategoryNode.objects.filter(id=id)
            try:
                queryset[0]
            except IndexError:
                return Response(
                    {'getNode_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST
                )
            serializers = NodeSerializerArticleId(queryset, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response({'getNode_Error': 'ValueError'}, status=status.HTTP_400_BAD_REQUEST)


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
        articles_id = []
        art = []
        key_word_found = []
        word = self.request.query_params.get('word')
        word_split = word.split(' ')
        if word:
            for word in word_split:
                key_word_found.append(Keywords.objects.filter(text__istartswith=word).values('id')[0]['id'])
            print(key_word_found)
            for keyword in key_word_found:
                keyword_A = Keyword_Article.objects.filter(keywords_id=keyword).values('article_id')
                if not keyword_A:
                    continue
                else:
                    articles_id = [ids for ids in keyword_A]
            for i in range(len(articles_id)):
                a = Article.objects.filter(id=articles_id[i]['article_id']).values()[0]
                art.append(a)
            return Response(art)
        else:
            return Response({'getArticlesByKeyWords_Error': "ValueError"}, status=status.HTTP_400_BAD_REQUEST)



class getArticlesByNode(APIView):
    serializer_class = ArticleSerializer

    node_id_param_config = openapi.Parameter(
        'node_id',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[node_id_param_config])
    def get(self, request):
        node_id = self.request.query_params.get('node_id')
        filter_by_id = CategoryNode.objects.filter(id=node_id).values('articles')[0]['articles']
        try:
            filter_by_id
        except IndexError:
            return Response({'getArticlesByNode_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST)
        if CategoryNode.objects.filter(id=node_id).values('final')[0]['final']:
            last_articles = Article.objects.filter(id=filter_by_id).values()
            return Response(last_articles)
        else:
            return Response({'getArticlesByNode': 'В этой категории final!=True'}, status=status.HTTP_404_NOT_FOUND)
