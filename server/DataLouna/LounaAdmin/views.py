from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article, CategoryNode, Keywords, KeywordArticle, modelUser
from .serializer import NodeSerializer, ArticleSerializer, NodeSerializerArticleId, UserSerializer


def RedirectToAdmin(request):
    return redirect('/admin/')


class getArticle(APIView):
    id_param_config = openapi.Parameter('id', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response", examples={"application/json": {"Article object": "id,title,text,photo"}}
        ),
        "404": openapi.Response(description="404 Response", examples={'getArticle_Error': 'ID not found'}),
    }


    @swagger_auto_schema(manual_parameters=[id_param_config], responses=response_schema_dict)
    def get(self, request):
        try:
            param_id = self.request.query_params.get('id')
        except ValueError:
            return Response({'ValueError'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Article.objects.filter(id=param_id).values()[0]
            return Response(instance)
        except IndexError:
            return Response({'getArticle_Error': 'ID not found'}, status=status.HTTP_404_NOT_FOUND)


class getChildren(APIView):
    serializer_class = NodeSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"CategoryNode object": "id,name,parent,final,valid"}},
        ),
        "400": openapi.Response(description="400 Response", examples={'getChildren_Error': 'ID not found'}),
    }

    parent_param_config = openapi.Parameter(
        'parent_id',
        in_=openapi.IN_QUERY,
        description='Получить ребенка родителя',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[parent_param_config], responses=response_schema_dict)
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
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"CategoryNode object": "id,name,parent,final,valid"}},
        ),
        "400": openapi.Response(
            description="400 Response",
        ),
    }

    id_param_config = openapi.Parameter(
        'id', in_=openapi.IN_QUERY, description='Получение узла', type=openapi.TYPE_STRING
    )


    @swagger_auto_schema(manual_parameters=[id_param_config], responses=response_schema_dict)
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
            return Response({'getNode_Error': 'ValueError'}, status=status.HTTP_400_BAD_REQUEST)


class getArticlesByKeyWords(APIView):
    serializer_class = NodeSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response", examples={"application/json": {"Article object": "id,title,text,photo"}}
        ),
        "400": openapi.Response(
            description="404 Response",
        ),
        "404": openapi.Response(description="400 Response"),
    }

    word_param_config = openapi.Parameter(
        'word',
        in_=openapi.IN_QUERY,
        description='Ключевые слова',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[word_param_config], responses=response_schema_dict)
    def get(self, request):
        articles_by_keywords = []
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
                articles_by_keywords.append(
                    set(
                        i['article_id'] for i in KeywordArticle.objects.filter(keywords_id=word.id).values('article_id')
                    )
                )
            if not articles_by_keywords:
                return Response(status=status.HTTP_404_NOT_FOUND)
            result = articles_by_keywords[0]
            for i in articles_by_keywords[1:]:
                result = result & i

            else:
                articles = Article.objects.filter(id__in=result).values()
                return Response(articles)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class getArticlesByNode(APIView):
    serializer_class = ArticleSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response", examples={"application/json": {"Article object": "id,title,text,photo"}}
        ),
        "404": openapi.Response(
            description="404 Response",
            examples={"application/json": {"getArticlesByNode_Error": "В этой категории final!=True"}},
        ),
    }

    node_id_param_config = openapi.Parameter(
        'node_id',
        in_=openapi.IN_QUERY,
        description='Поиск по ID узла',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[node_id_param_config], responses=response_schema_dict)
    def get(self, request):
        node_id = self.request.query_params.get('node_id')
        filter_by_id = CategoryNode.objects.filter(id=node_id).values('articles')[0]['articles']
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
    serializer_class = UserSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={
                "application/json": {
                    "chat_id": "1111",
                    "site_id": "2222",
                    "subscription_status": "FIRST",
                    "subscription_paid_date": "DD-MM-YYYY",
                    "subscription_end_date": "DD-MM-YYYY",
                }
            },
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="chat_id",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="ID из бота",
            ),
            openapi.Parameter(
                name='site_id',
                type="integer",
                in_=openapi.TYPE_INTEGER,
                description="ID на сайте",
            ),
            openapi.Parameter(
                name='subscription_status',
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="При создании ZERO, при апдейте либо "
                "FIRST(Не оформил триал),"
                "либо SECOND(Триал оформлен),"
                "либо THIRD(Оформил (продлил?) подписку)"
                "либо FOURTH(Карта удалена сразу)",
            ),
            openapi.Parameter(
                name='subscription_paid_date',
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="Дата оплаты подписки, формат DD-MM-YYYY",
            ),
            openapi.Parameter(
                name='subscription_end_date',
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="Дата окончания подписки, формат DD-MM-YYYY",
            ),
        ],
        responses=response_schema_dict,

    )
    def get(self, request):
        site_id = request.GET.get('site_id')
        chat_id = request.GET.get('chat_id')
        subscription_status = request.GET.get('subscription_status')
        subscription_paid_date = request.GET.get('subscription_paid_date')
        subscription_end_date = request.GET.get('subscription_end_date')
        same_rec = modelUser.objects.filter(chat_id=chat_id).values('chat_id')
        if not same_rec.exists():
            modelUser.objects.create(
                site_id=None,
                chat_id=chat_id,
                subscription_status='ZERO',
                subscription_paid_date=None,
                subscription_end_date=None,
            )
            instance = modelUser.objects.filter(chat_id=chat_id).values()
            return Response(instance)

        if same_rec.exists():
            modelUser.objects.filter(chat_id=chat_id).update(
                site_id=site_id,
                chat_id=chat_id,
                subscription_status=subscription_status,
                subscription_paid_date=subscription_paid_date,
                subscription_end_date=subscription_end_date,
            )
            instance = modelUser.objects.filter(chat_id=chat_id).values()
            return Response(instance)


class getUser(APIView):
    serializer_class = UserSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={
                "application/json": {
                    "chat_id": "1111",
                    "site_id": "2222",
                    "subscription_status": "FIRST",
                    "subscription_paid_date": "DD-MM-YYYY",
                    "subscription_end_date": "DD-MM-YYYY",
                }
            },
        ),
        "404": openapi.Response(
            description="404 Response", examples={"application/json": {'getUser_Error': 'ID not found'}}
        ),
    }
    get_user_config = openapi.Parameter(
        'chat_id',
        in_=openapi.IN_QUERY,
        description='Получение пользователя по chat_id',
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[get_user_config], responses=response_schema_dict)
    def get(self, request):
        chat_id = self.request.query_params.get('chat_id')
        user = modelUser.objects.filter(chat_id=chat_id).values()
        try:
            user[0]
        except IndexError:
            return Response({'getUser_Error': 'ID not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(user)
