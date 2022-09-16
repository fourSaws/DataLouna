from django.shortcuts import redirect
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Article, CategoryNode, Keywords, Keyword_Article
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
        return Response(
            {'getArticle_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST
        )


class getChildren(viewsets.ViewSet):
    def list(self, request):
        parent_id = self.request.query_params.get('parent_id')
        queryset = CategoryNode.objects.filter(parent_id=parent_id)
        try:
            queryset[0]
        except IndexError:
            return Response(
                {'getChildren_Error': 'ID not found'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class getNode(viewsets.ViewSet):
    def list(self, request):
        id = self.request.query_params.get('id')
        queryset = CategoryNode.objects.filter(id=id)
        try:
            queryset[0]
        except IndexError:
            return Response(
                {'getNode_Error': 'ID not found'}, status=status.HTTP_400_BAD_REQUEST
            )
        serializer = NodeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class getArticlesByKeyWords(viewsets.ViewSet):
    def list(self, request):
        word = self.request.query_params.get('word')
        id_by_word = Keywords.objects.filter(text=word).values('id')[0]
        print(f"{id_by_word=}")
        keyword_A = Keyword_Article.objects.filter(keywords_id=id_by_word['id']).values(
            'article_id'
        )
        print(f"{keyword_A=}")
        print(len(keyword_A))
        article_array = []
        for i in range(len(keyword_A)):
            Articles = Article.objects.filter(id=keyword_A[i]['article_id']).values()[0]
            article_array.append(Articles)
        return Response(article_array)
