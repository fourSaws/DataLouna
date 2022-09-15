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




class getChildren(viewsets.ViewSet):
        def list(self,request):
            parent_id = self.request.query_params.get('parent_id')
            queryset = CategoryNode.objects.filter(parent_id=parent_id)
            try:
                queryset[0]
            except IndexError:
                return Response({'getChildren_Error':'ID not found'},status=status.HTTP_400_BAD_REQUEST)
            serializer = NodeSerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)


class getNode(viewsets.ViewSet):
    def list(self, request):
        id = self.request.query_params.get('id')
        queryset = CategoryNode.objects.filter(id=id)
        try:
            queryset[0]
        except IndexError:
            return Response({'getNode_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




