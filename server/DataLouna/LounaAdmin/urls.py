from django.contrib import admin
from django.urls import path
from .views import RedirectToAdmin

app_name = 'LounaAdmin'
urlpatterns = [
    path('',RedirectToAdmin),
]