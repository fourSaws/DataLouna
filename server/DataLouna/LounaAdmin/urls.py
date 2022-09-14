from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import RedirectToAdmin,getArticles

app_name = 'LounaAdmin'
urlpatterns = [
    path('',RedirectToAdmin),
    path('api/getArticles',getArticles),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)