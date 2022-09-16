from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Article,Keywords,CategoryNode,Keyword_Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','title','text','photo','get_html_photo')

    def get_html_photo(self, obj):
        if obj.photo:
            print(obj.photo.url)
            return mark_safe(f'<img src="{obj.photo.url}" style="max-width:100px">')
        else:
            return mark_safe('<img src= "default.jpg">')

    get_html_photo.short_description = 'Миниатюра'


class KeywordsAdmin(admin.ModelAdmin):
    list_display = ('id','text')

class CategoryNodeAdmin(admin.ModelAdmin):
    list_display = ('id','name','admin_names','parent','articles','valid')
    filter_horizontal = ['children']

class KeywordsArticleAdmin(admin.ModelAdmin):
    list_display = ('id','keywords_id','article_id',)

admin.site.register(Article,ArticleAdmin)
admin.site.register(Keywords,KeywordsAdmin)
admin.site.register(CategoryNode,CategoryNodeAdmin)
admin.site.register(Keyword_Article,KeywordsArticleAdmin)

