from django.http import Http404
from django.shortcuts import render, redirect
from rest_framework import status, viewsets, exceptions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Article,CategoryNode
from .serializer import NodeSerializer

def RedirectToAdmin(request):
    return redirect('/admin/')


@api_view(['GET'])
@permission_classes([AllowAny])
def getArticles(request):
    param_id = request.query_params['id']
    try:
        instance = Article.objects.filter(id=param_id).values()[0]
        return Response(instance)
    except IndexError:
        return Response({'getArticle_Error':'ID not found'},status=status.HTTP_400_BAD_REQUEST)




class getChildren(viewsets.ReadOnlyModelViewSet):
        def get_queryset(self):
            parent_id = self.request.query_params.get('parent_id')
            queryset = CategoryNode.objects.filter(parent_id=parent_id).values()[0]
            return queryset
        serializer_class = NodeSerializer


class getNode(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        id = self.request.query_params.get('id')
        queryset = CategoryNode.objects.filter(id=id)
        return queryset
    serializer_class = NodeSerializer

    def permission_denied(self, request, message=None, code=None):
        if request.authenticators and not request.successful_authenticator:
            raise  exceptions.NotAuthenticated()
        raise exceptions.NotAcceptable(detail=message)




