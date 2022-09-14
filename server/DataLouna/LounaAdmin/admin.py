from django.contrib import admin
from .models import Article,Keywords,CategoryNode,Keyword_Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','text','photo')


class KeywordsAdmin(admin.ModelAdmin):
    list_display = ('id','text')

class CategoryNodeAdmin(admin.ModelAdmin):
    list_display = ('id','name','children','parent','articles','valid')

class KeywordsArticleAdmin(admin.ModelAdmin):
    list_display = ('id','keywords_id','article_id',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Keywords,KeywordsAdmin)
admin.site.register(CategoryNode,CategoryNodeAdmin)
admin.site.register(Keyword_Article,KeywordsArticleAdmin)

