from django.contrib import admin

from article.models import Article, ArticleIndex

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'title', 'fid_func','cate_id_func', 'date_update', 'date_create')
    search_fields = ['title', 'content']
    list_filter = ['date_create', 'username', 'fid', 'cate_id']
class ArticleIndexAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','username', 'cate_id_func', 'date_create')
    search_fields = ['title']
    list_filter = ['date_create', 'username', 'cate_id']

admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleIndex, ArticleIndexAdmin)
