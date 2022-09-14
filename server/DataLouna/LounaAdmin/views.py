from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Article,CategoryNode

def RedirectToAdmin(request):
    return redirect('/admin/')


@api_view(['GET'])
@permission_classes([AllowAny])
def getArticles(request):
    param_id = request.query_params['id']
    instance = Article.objects.filter(id=param_id).values()
    return Response(instance)


