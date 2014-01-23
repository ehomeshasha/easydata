from django.contrib import admin

from pdf.models import pdf, Mark, Comment

class pdfAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename','title', 'cate_id_func','filesize_func', 'filepn', 'views', 'mark', 'comment', 'date_upload')
    search_fields = ['title', 'description', 'filename']
    list_filter = ['date_upload', 'cate_id','username']
class MarkAdmin(admin.ModelAdmin):
    list_display = ('mid', 'username', 'pdf_id_func', 'date_create')
    search_fields = ['content']
    list_filter = ['date_create', 'pdf_id', 'username']
   
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','username', 'pdf_id_func', 'rate_score', 'date_create')
    search_fields = ['title', 'content']
    list_filter = ['date_create', 'pdf_id', 'username', 'rate_score']

admin.site.register(pdf, pdfAdmin)
admin.site.register(Mark, MarkAdmin)
admin.site.register(Comment, CommentAdmin)