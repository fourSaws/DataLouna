from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, CategoryNode, Keywords, Keyword_Article
from .serializer import NodeSerializer,ArticleSerializer,NodeSerializerArticleId


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
        final_array = []
        parent_id = self.request.query_params.get('parent_id')
        queryset = CategoryNode.objects.filter(parent_id=parent_id)
        try:
            queryset[0]
        except IndexError:
            return Response(
                {'getChildren_Error': 'ID not found'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        for i in range(len(queryset.values('final'))):
            final_array.append(queryset.values('final')[i]['final'])
        if False not in final_array:
            serializer = NodeSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = NodeSerializerArticleId(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


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
            print(f"{queryset.values()[0]['final']=}")
            if queryset.values()[0]['final']:
                serializer = NodeSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer_ = NodeSerializerArticleId(queryset,many=True)
                return Response(serializer_.data,status=status.HTTP_200_OK)
        else:
            return Response({'getNode_Error':'ValueError'},status=status.HTTP_400_BAD_REQUEST)



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
        if word:
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
        else:
            return Response({'getArticlesByKeyWords_Error':"ValueError"},status=status.HTTP_400_BAD_REQUEST)

class getArticlesByNode(APIView):
    serializer_class = ArticleSerializer

    node_id_param_config = openapi.Parameter(
        'node_id',
        in_=openapi.IN_QUERY,
        description='Description',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[node_id_param_config])
    def get(self,request):
        node_id = self.request.query_params.get('node_id')
        filter_by_id = CategoryNode.objects.filter(id=node_id).values('articles')[0]['articles']
        try:
            filter_by_id
        except IndexError:
            return Response({'getArticlesByNode_Error':'ID not found'},status=status.HTTP_400_BAD_REQUEST)

        if CategoryNode.objects.filter(id=node_id).values('final')[0]['final']:
            last_articles = Article.objects.filter(id=filter_by_id).values()
            return Response(last_articles)
        else:
            return Response({'getArticlesByNode':'Это не конечная статья'},status=status.HTTP_400_BAD_REQUEST)
