from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, CategoryNode, Keywords, KeywordArticle,User
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
        queryset = CategoryNode.objects.filter(parent_id=parent_id).filter(valid=True)
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
            queryset = CategoryNode.objects.filter(id=id).filter(valid=True)
            try:
                queryset[0]
            except IndexError:
                return Response(
                    {'getNode_Error': 'ID not found'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializers = NodeSerializerArticleId(queryset, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'getNode_Error': 'ValueError'}, status=status.HTTP_400_BAD_REQUEST
            )


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
        articles_by_keywords = []
        result = []
        keyword_found = []
        word = self.request.query_params.get('word')
        if word:
            word_split = word.split(' ')
            for word in word_split:
                for keyword in Keywords.objects.filter(text__istartswith=word):
                    keyword_found.append(keyword)
            if not word_split:
                return Response(status=status.HTTP_404_NOT_FOUND)
            for word in keyword_found:
                articles_by_keywords.append(set(i['article_id'] for i in KeywordArticle.objects.filter(keywords_id=word.id).values('article_id')))
            if not articles_by_keywords:
                return Response(status=status.HTTP_404_NOT_FOUND)
            result = articles_by_keywords[0]
            print(result)
            for i in articles_by_keywords[1:]:
                result = result & i
                print(result)

            else:
                articles = Article.objects.filter(id__in=result).values()
                return Response(articles)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
        filter_by_id = CategoryNode.objects.filter(id=node_id).values('articles')[0][
            'articles'
        ]
        try:
            filter_by_id
        except IndexError:
            return Response(
                {'getArticlesByNode_Error': 'ID not found'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if CategoryNode.objects.filter(id=node_id).values('final')[0]['final']:
            last_articles = Article.objects.filter(id=filter_by_id).values()
            return Response(last_articles)
        else:
            return Response(
                {'getArticlesByNode': 'В этой категории final!=True'},
                status=status.HTTP_404_NOT_FOUND,
            )

class createUser(APIView):
    def get(self,request):
        site_id = self.request.query_params.get('site_id')
        chat_id = self.request.query_params.get('chat_id')
        subscription_status = self.request.query_params.get('subscription_status')
        subscription_paid_date = self.request.query_params.get('subscription_paid_date')
        subscription_end_date = self.request.query_params.get('subscription_end_date')
        id_check = User.objects.filter(chat_id=chat_id).values()
        if not id_check.exists():
            User.objects.create(site_id=site_id,chat_id=chat_id,subscription_status=subscription_status,subscription_paid_date=subscription_paid_date,subscription_end_date=subscription_end_date)
            instance = User.objects.filter(chat_id=chat_id).values()
            return Response(instance)
        else:
            User.objects.update(subscription_status=subscription_status,subscription_paid_date=subscription_paid_date,subscription_end_date=subscription_end_date)
            instance = User.objects.filter(chat_id=chat_id).values()
            return Response(instance)


class getUser(APIView):

    def get(self,request):
        chat_id = self.request.query_params.get('chat_id')
        user = User.objects.filter(chat_id=chat_id).values()
        try:
            user[0]
        except IndexError:
            return Response({"getUser_Error":"ID not found"},status=status.HTTP_404_NOT_FOUND)
        return Response(user)


