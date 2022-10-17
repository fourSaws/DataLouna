from django.shortcuts import redirect, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Article,
    CategoryNode,
    Keywords,
    KeywordArticle,
    modelUser,
    NoviceNewsTellers,
    InactiveNewsTellers,
)
from .serializer import (
    NodeSerializer,
    ArticleSerializer,
    NodeSerializerArticleId,
    UserSerializer,
)


def RedirectToAdmin(request):
    return redirect("/admin/")


class NotificationRender(APIView):
    permission_classes = [IsAuthenticated]

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
    def get(self, request):
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
                return Response({"Notification_error": "Можно выбирать либо chat_id или status_frist"})

        else:
            return render(request, "html/Notification_page.html")


class getArticle(APIView):
    permission_classes = [IsAuthenticated]

    id_param_config = openapi.Parameter("id", in_=openapi.IN_QUERY, description="Description", type=openapi.TYPE_STRING)
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Article object": "id,title,text,photo"}},
        ),
        "404": openapi.Response(description="404 Response", examples={"getArticle_Error": "ID not found"}),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                in_=openapi.IN_QUERY,
                description="Description",
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
            instance = Article.objects.filter(id=param_id).values()[0]
            return Response(instance)
        except IndexError:
            return Response({"getArticle_Error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)


class getChildren(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NodeSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"CategoryNode object": "id,name,parent,final,valid"}},
        ),
        "400": openapi.Response(description="400 Response", examples={"getChildren_Error": "ID not found"}),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "parent_id",
                in_=openapi.IN_QUERY,
                description="Получить ребенка родителя",
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
        parent_id = self.request.query_params.get("parent_id")
        queryset = CategoryNode.objects.filter(parent_id=parent_id).filter(valid=True)
        try:
            queryset[0]
        except IndexError:
            return Response(
                {"getChildren_Error": "ID not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializers = NodeSerializerArticleId(queryset, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class getNode(APIView):
    permission_classes = [IsAuthenticated]
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
        "id",
        in_=openapi.IN_QUERY,
        description="Получение узла",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                in_=openapi.IN_QUERY,
                description="Получение узла",
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
        id = self.request.query_params.get("id")
        if id:
            queryset = CategoryNode.objects.filter(id=id).filter(valid=True)
            try:
                queryset[0]
            except IndexError:
                return Response(
                    {"getNode_Error": "ID not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializers = NodeSerializerArticleId(queryset, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            return Response({"getNode_Error": "ValueError"}, status=status.HTTP_400_BAD_REQUEST)


class getArticlesByKeyWords(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NodeSerializer
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
        articles_by_keywords = []
        keyword_found = []
        word = self.request.query_params.get("word")
        if word:
            word_split = word.split(" ")
            for word in word_split:
                for keyword in Keywords.objects.filter(text__istartswith=word):
                    keyword_found.append(keyword)
            if not word_split:
                return Response(status=status.HTTP_404_NOT_FOUND)
            for word in keyword_found:
                articles_by_keywords.append(
                    set(
                        i["article_id"] for i in KeywordArticle.objects.filter(keywords_id=word.id).values("article_id")
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
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Article object": "id,title,text,photo"}},
        ),
        "404": openapi.Response(
            description="404 Response",
            examples={"application/json": {"getArticlesByNode_Error": "В этой категории final!=True"}},
        ),
    }

    node_id_param_config = openapi.Parameter(
        "node_id",
        in_=openapi.IN_QUERY,
        description="Поиск по ID узла",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "node_id",
                in_=openapi.IN_QUERY,
                description="Поиск по ID узла",
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
        node_id = self.request.query_params.get("node_id")
        filter_by_id = CategoryNode.objects.filter(id=node_id).values("articles")[0]["articles"]
        try:
            filter_by_id
        except IndexError:
            return Response(
                {"getArticlesByNode_Error": "ID not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if CategoryNode.objects.filter(id=node_id).values("final")[0]["final"]:
            last_articles = Article.objects.filter(id=filter_by_id).values()
            return Response(last_articles)
        else:
            return Response(
                {"getArticlesByNode": "В этой категории final!=True"},
                status=status.HTTP_404_NOT_FOUND,
            )


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
                name="subscription_paid_date",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="Дата оплаты подписки, формат DD-MM-YYYY",
            ),
            openapi.Parameter(
                name="subscription_end_date",
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="Дата окончания подписки, формат DD-MM-YYYY",
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
        subscription_paid_date = request.GET.get("subscription_paid_date")
        subscription_end_date = request.GET.get("subscription_end_date")
        same_rec = modelUser.objects.filter(chat_id=chat_id).values("chat_id")
        if not same_rec.exists():
            modelUser.objects.create(
                site_id=None,
                chat_id=chat_id,
                subscription_status="ZERO",
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
                    "subscription_paid_date": "DD-MM-YYYY",
                    "subscription_end_date": "DD-MM-YYYY",
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
        user = modelUser.objects.filter(chat_id=chat_id).values()
        try:
            user[0]
        except IndexError:
            return Response({"getUser_Error": "ID not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(user)


class getNoviceNewsTellers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get("id")
        if id:
            novice_news_tellers = NoviceNewsTellers.objects.filter(id=id).values()
            return Response(novice_news_tellers)
        else:
            novice_news_tellers = NoviceNewsTellers.objects.all().values()
            return Response(novice_news_tellers)


class getInactiveNewsTellers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.GET.get("id")
        if id:
            inactive_news_tellers = InactiveNewsTellers.objects.filter(id=id).values()
            return Response(inactive_news_tellers)
        else:
            inactive_news_tellers = InactiveNewsTellers.objects.all().values()
            return Response(inactive_news_tellers)


class onEnter(APIView):
    permission_classes = [IsAuthenticated]
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Пользователь существует": "True"}},
        ),
        "400": openapi.Response(
            description="400 Response",
            examples={"application/json": {"Пользователь не существует": "False"}},
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "chat_id",
                in_=openapi.IN_QUERY,
                required=True,
                description="Получение пользователя по chat_id",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="site_id",
                type="integer",
                required=True,
                in_=openapi.TYPE_INTEGER,
                description="ID на сайте",
            ),
            openapi.Parameter(
                name="status",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="ZERO(Нет аккаунта на сайте)"
                            "FIRST(Не оформил триал),"
                            "SECOND(Триал оформлен),"
                            "THIRD(Оформил (продлил?) подписку)"
                            "FOURTH(Карта удалена сразу)",
            ),
            openapi.Parameter(
                name="subscription_end_date",
                required=False,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="YYYY-MM-DD",
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
        site_id = self.request.query_params.get("site_id")
        status_ = self.request.query_params.get("status")
        subscription_end_date = self.request.query_params.get("subscription_end_date")

        user_exists = modelUser.objects.filter(chat_id=chat_id)
        if user_exists.exists():
            user_exists.update(
                site_id=site_id,
                subscription_status=status_,
            )
            if status_ != "ZERO" and status_ != "FIRST" and subscription_end_date:
                user_exists.update(
                    site_id=site_id,
                    subscription_status=status_,
                    subscription_end_date=subscription_end_date
                )
                return Response({"Пользователь существует и статус подписки != ZERO или FIRST": True},
                                status=status.HTTP_200_OK)
            elif status_ != "ZERO" and status_ != "FIRST" and subscription_end_date is None:
                return Response("Если статус не равен ZERO или FIRST, то нужно передавать subscription_end_date",
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                user_exists.update(
                    site_id=site_id,
                    subscription_status=status_,
                    subscription_end_date=None
                )
                return Response({f"Пользователь существует но статус подписки равен {status_}": True},
                                status=status.HTTP_200_OK)
        else:
            return Response({"Пользователь не существует": False}, status=status.HTTP_400_BAD_REQUEST)


class subscriptionPaid(APIView):
    permission_classes = [IsAuthenticated]
    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Запись произведина успешно": "True"}},
        ),
        "404": openapi.Response(
            description="404 Response",
            examples={"application/json": {"Пользователь не найден": "False"}},
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "site_id",
                in_=openapi.IN_QUERY,
                description="ID на сайте",
                required=True,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="status",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="ZERO(Нет аккаунта на сайте)"
                            "FIRST(Не оформил триал),"
                            "SECOND(Триал оформлен),"
                            "THIRD(Оформил (продлил?) подписку)"
                            "FOURTH(Карта удалена сразу)",
            ),
            openapi.Parameter(
                name="subscription_end_date",
                required=False,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="YYYY-MM-DD",
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
        site_id = self.request.query_params.get("site_id")
        status_ = self.request.query_params.get("status")
        subscription_end_date = self.request.query_params.get("subscription_end_date")

        status_check = modelUser.objects.filter(site_id=site_id)

        if status_check.exists() and status_ in ("ZERO", "FIRST", "SECOND", "THIRD", "FOURTH"):
            status_check.update(
                site_id=site_id,
                subscription_status=status_,
            )
            if status_ != "ZERO" and status_ != "FIRST" and subscription_end_date:
                status_check.update(
                    site_id=site_id,
                    subscription_status=status_,
                    subscription_end_date=subscription_end_date
                )
                return Response("Запись произведина успешно", status=status.HTTP_200_OK)
            elif status_ != "ZERO" and status_ != "FIRST" and subscription_end_date is None:
                return Response("Если статус не равен ZERO, то нужно передавать subscription_end_date",
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                status_check.update(
                    site_id=site_id,
                    subscription_status=status_,
                    subscription_end_date=None
                )
                return Response(f"Статус равен {status_}")
        elif status_ not in ("ZERO", "FIRST", "SECOND", "THIRD", "FOURTH"):
            return Response("Неверный статус", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)


class updateStatus(APIView):
    permission_classes = [IsAuthenticated]

    response_schema_dict = {
        "200": openapi.Response(
            description="200 Response",
            examples={"application/json": {"Статус обновлен": "True"}},
        ),
        "400": openapi.Response(
            description="400 Response",
            examples={"application/json": {"Неверный статус": "False"}},
        ),
        "404": openapi.Response(
            description="400 Response",
            examples={"application/json": {"Пользователь не найден": "False"}},
        ),
    }

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "site_id",
                in_=openapi.IN_QUERY,
                description="ID на сайте",
                required=True,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="new_status",
                required=True,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="ZERO(Нет аккаунта на сайте)"
                            "FIRST(Не оформил триал),"
                            "SECOND(Триал оформлен),"
                            "THIRD(Оформил (продлил?) подписку)"
                            "FOURTH(Карта удалена сразу)",
            ),
            openapi.Parameter(
                name="subscription_end_date",
                required=False,
                type=openapi.TYPE_STRING,
                in_=openapi.IN_QUERY,
                description="YYYY-MM-DD",
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
        site_id = self.request.query_params.get("site_id")
        new_status = self.request.query_params.get("new_status")
        subscription_end_date = self.request.query_params.get("subscription_end_date")
        user_check = modelUser.objects.filter(site_id=site_id)
        if user_check.exists() and new_status in ("ZERO", "FIRST", "SECOND", "THIRD", "FOURTH"):
            user_check.update(
                site_id=site_id,
                subscription_status=new_status,
            )
            if new_status != "ZERO" and new_status != "FIRST" and subscription_end_date:
                user_check.update(
                    site_id=site_id,
                    subscription_status=new_status,
                    subscription_end_date=subscription_end_date
                )
                return Response("Статус обновлен", status=status.HTTP_200_OK)
            elif new_status != "ZERO" and new_status != "FIRST" and subscription_end_date is None:
                return Response("Если статус не равен ZERO или FIRST, то нужно передавать subscription_end_date",
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                user_check.update(
                    site_id=site_id,
                    subscription_status=new_status,
                    subscription_end_date=None
                )
                return Response(f"Статус обновлен на {new_status}", status=status.HTTP_200_OK)
        elif new_status not in ("ZERO", "FIRST", "SECOND", "THIRD", "FOURTH"):
            return Response("Неверный статус", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Пользователь не найден", status=status.HTTP_404_NOT_FOUND)
