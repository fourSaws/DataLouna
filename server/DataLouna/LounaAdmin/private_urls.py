from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    RedirectToAdmin,
    getArticle,
    getArticlesByKeyWords,
    createUser,
    getUser,
    NotificationRender,
    TopArticles,
)

urlpatterns = [
    path("", RedirectToAdmin),
    path("api/getArticle", getArticle.as_view()),
    path("api/getArticlesByKeyWords", getArticlesByKeyWords.as_view()),
    path("api/createUser", createUser.as_view()),
    path("api/getUser", getUser.as_view()),
    path("notification/", NotificationRender.as_view()),
    path("api/topArticles", TopArticles.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
