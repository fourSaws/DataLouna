from datetime import datetime, date, timedelta

from django.db.models import QuerySet
from django.shortcuts import redirect, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from DataLounaNotifications.models import Quiz, QuizQuestions, QuestionAnswers, EventsNotifications
from LounaAdmin import onetimeMailing
from .models import (
    Article,
    Keywords,
    KeywordArticle,
    User,
    NoviceNewsTellers,
)
from .onetimeMailing import quiz, one_timeMailing
from .serializer import UserSerializer, TopSerializer


def RedirectToAdmin(request):
    return redirect("/admin/")


class NotificationRender(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                description="Authorization token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_HEADER,
            ),
        ],
    )
    def post(self, request):
        chat_id = request.POST.get("chat-id")
        status_zero = request.POST.get("ZERO")
        status_first = request.POST.get("FIRST")
        status_second = request.POST.get("SECOND")
        status_third = request.POST.get("THIRD")
        status_fourth = request.POST.get("FOURTH")
        status_exists = bool(status_zero or status_first or status_second or status_third or status_fourth)
        notification = request.POST.get("notification-area")
        if request.method == "POST":
            if chat_id and notification and not status_exists:
                return Response(data={"chat-id": chat_id, "notification-area": notification})
            if status_exists and not chat_id:
                return Response(
                    data={
                        "statuses": list(
                            i
                            for i in (
                                status_zero,
                                status_first,
                                status_second,
                                status_third,
                                status_fourth,
                            )
                            if i
                        ),
                        "notification": notification,
                    }
                )
            if not chat_id and not status_exists and not notification:
                return Response("123")
            if chat_id and status_exists:
                return Response({"Notification_error": "Можно выбирать либо chat_id или status_first"})

        else:
            return render(request, "html/Notification_page.html")


class getArticle(APIView):
    permission_classes = [IsAuthenticated]

    id_param_config = openapi.Parameter(
        "id",
        in_=openapi.IN_QUERY,
        description="Get Article object by id",
        type=openapi.TYPE_STRING,
    )
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Article object": "id,title,text,photo,links[list(Article objects)]"}},
        ),
        "404": openapi.Response(description="404 Response", examples={"getArticle_Error": "ID not found"}),
        "400": openapi.Response(description="400 Response", examples={"ValueError": "Bad param"}),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                in_=openapi.IN_QUERY,
                description="ID of Article object",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="Authorization",
                description="Authorization token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_HEADER,
            ),
        ],
        responses=response_schema_dict,
    )
    def get(self, request):
        try:
            param_id = self.request.query_params.get("id")
        except ValueError:
            return Response({"ValueError"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            instance = Article.objects.filter(id=param_id)
            serializer = TopSerializer(instance, many=True)
            return Response(serializer.data)
        except IndexError:
            return Response({"getArticle_Error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)


class TopArticles(APIView):
    permission_classes = [IsAuthenticated]
    id_param_config = openapi.Parameter(
        "id",
        in_=openapi.IN_QUERY,
        description="Get Article object where top = True",
        type=openapi.TYPE_STRING,
    )
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Article object": "id,title,text,photo,links[Article objects]"}},
        ),
        "404": openapi.Response(description="404 Response", examples={"getArticle_Error": "ID not found"}),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                description="Authorization token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_HEADER,
            ),
        ],
        responses=response_schema_dict,
    )
    def get(self, request):
        try:
            instance = Article.objects.filter(on_top=True)
            serializer = TopSerializer(instance, many=True)
            return Response(serializer.data)
        except IndexError:
            return Response({"getArticle_Error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)


class getArticlesByKeyWords(APIView):
    permission_classes = [IsAuthenticated]
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Article object": "id,title,text,photo"}},
        ),
        "400": openapi.Response(
            description="404 Response",
        ),
        "404": openapi.Response(description="400 Response"),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "word",
                in_=openapi.IN_QUERY,
                description="Ключевые слова",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="Authorization",
                description="Authorization token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_HEADER,
            ),
        ],
        responses=response_schema_dict,
    )
    def get(self, request):
        word = self.request.query_params.get("word").lower()
        if word:
            keyword_found = Keywords.objects.filter(text__icontains=word)
            if not keyword_found:
                return Response(status=status.HTTP_404_NOT_FOUND)
            articles = KeywordArticle.objects.none()
            for word in keyword_found:
                articles = articles | KeywordArticle.objects.filter(keywords_id=word)
            article = [i.article_id.id for i in articles]
            return Response(Article.objects.filter(id__in=article).values())
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class createUser(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={
                "application/json": {
                    "chat_id": "1111",
                    "site_id": "2222",
                    "subscription_status": "FIRST",
                    "subscription_end_date": "DD-MM-YYYY%20H:M:S",
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
                name="site_id",
                type="integer",
                in_=openapi.TYPE_INTEGER,
                description="ID на сайте",
            ),
            openapi.Parameter(
                name="subscription_status",
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
                name="subscription_end_date",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="Дата окончания подписки, формат DD-MM-YYYY%20H:M:S",
            ),
            openapi.Parameter(
                name="Authorization",
                description="Authorization token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_HEADER,
            ),
        ],
        responses=response_schema_dict,
    )
    def get(self, request):
        site_id = request.GET.get("site_id")
        chat_id = request.GET.get("chat_id")
        subscription_status = request.GET.get("subscription_status")
        subscription_end_date = request.GET.get("subscription_end_date")
        same_rec = User.objects.filter(chat_id=chat_id).values("chat_id")
        if not same_rec.exists():
            User.objects.create(
                site_id=None,
                chat_id=chat_id,
                subscription_status="ZERO",
                subscription_end_date=None,
            )
            instance = User.objects.filter(chat_id=chat_id).values()
            return Response(instance)

        if same_rec.exists():
            User.objects.filter(chat_id=chat_id).update(
                site_id=site_id,
                chat_id=chat_id,
                subscription_status=subscription_status,
                subscription_end_date=subscription_end_date,
            )
            instance = User.objects.filter(chat_id=chat_id).values()
            return Response(instance)


class getUser(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={
                "application/json": {
                    "chat_id": "1111",
                    "site_id": "2222",
                    "subscription_status": "FIRST",
                    "subscription_end_date": "DD-MM-YYYY%20H:M:S",
                }
            },
        ),
        "404": openapi.Response(
            description="404 Response",
            examples={"application/json": {"getUser_Error": "ID not found"}},
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "chat_id",
                in_=openapi.IN_QUERY,
                description="Получение пользователя по chat_id",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="Authorization",
                description="Authorization token",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_HEADER,
            ),
        ],
        responses=response_schema_dict,
    )
    def get(self, request):
        chat_id = self.request.query_params.get("chat_id")
        user = User.objects.filter(chat_id=chat_id).values()
        try:
            user[0]
        except IndexError:
            return Response({"getUser_Error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(user)
