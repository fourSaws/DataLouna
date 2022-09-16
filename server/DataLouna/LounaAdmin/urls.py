from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import RedirectToAdmin,getArticle,getChildren,getNode,getArticlesByKeyWords

app_name = 'LounaAdmin'
urlpatterns = [
    path('',RedirectToAdmin),
    path('api/getArticle',getArticle.as_view()),
    path('api/getChildren',getChildren.as_view()),
    path('api/getNode',getNode.as_view()),
    path('api/getArticlesByKeyWords',getArticlesByKeyWords.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
