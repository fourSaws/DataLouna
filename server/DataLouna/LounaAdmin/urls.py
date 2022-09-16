from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import (
    RedirectToAdmin,
    getArticles,
    getChildren,
    getNode,
    getArticlesByKeyWords,
)

app_name = 'LounaAdmin'
urlpatterns = [
    path('', RedirectToAdmin),
    path('api/getArticles', getArticles),
    path('api/getChildren', getChildren.as_view({'get': 'list'})),
    path('api/getNode', getNode.as_view({'get': 'list'})),
    path('api/getArticlesByKeyWords', getArticlesByKeyWords.as_view({'get': 'list'})),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
