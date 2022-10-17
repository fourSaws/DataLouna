from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    RedirectToAdmin,
    getArticle,
    getChildren,
    getNode,
    getArticlesByKeyWords,
    getArticlesByNode,
    createUser,
    getUser,
    getNoviceNewsTellers,
    NotificationRender,
    onEnter,
)

urlpatterns = [
    path("", RedirectToAdmin),
    path("api/getArticle", getArticle.as_view()),
    path("api/getChildren", getChildren.as_view()),
    path("api/getNode", getNode.as_view()),
    path("api/getArticlesByKeyWords", getArticlesByKeyWords.as_view()),
    path("api/getArticlesByNode", getArticlesByNode.as_view()),
    path("api/createUser", createUser.as_view()),
    path("api/getUser", getUser.as_view()),
    path("api/getNoviceNewsTellers", getNoviceNewsTellers.as_view()),
    path("notifications", NotificationRender.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
