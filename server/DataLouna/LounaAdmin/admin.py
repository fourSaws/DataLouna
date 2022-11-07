from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Article,
    Keywords,
    KeywordArticle,
    User,
    NoviceNewsTellers,
    InactiveNewsTellers,
    Notification,
)


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "text",
        'links_many_to_many',
        'on_top',
        "photo",
        "get_html_photo",
    )

    def get_html_photo(self, obj):
        if obj.photo:
            print(obj.photo.url)
            return mark_safe(f'<img src="{obj.photo.url}" style="max-width:100px">')
        else:
            return mark_safe('<img src= "default.jpg">')

    filter_horizontal = [
        "links",
    ]
    get_html_photo.short_description = "Миниатюра"


class KeywordsAdmin(admin.ModelAdmin):
    list_display = ("id", "text")


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "site_id",
        "chat_id",
        "subscription_status",
        "subscription_end_date",
    ]


class KeywordsArticleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "keywords_id",
        "article_id",
    )


class NoviceNewsTellersAdmin(admin.ModelAdmin):
    list_display = ("id", "after_time", "text")


class InactiveNewsTellersAdmin(admin.ModelAdmin):
    list_display = ("after_time", "text")


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("type", "text")


admin.site.register(Article, ArticleAdmin)
admin.site.register(Keywords, KeywordsAdmin)
admin.site.register(KeywordArticle, KeywordsArticleAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(NoviceNewsTellers, NoviceNewsTellersAdmin)
admin.site.register(InactiveNewsTellers, InactiveNewsTellersAdmin)
admin.site.register(Notification, NotificationAdmin)
