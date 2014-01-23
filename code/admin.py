from django.contrib import admin

from code.models import Code, Mark

class CodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'username','title','brush_func', 'cate_id_func', 'date_create')
    search_fields = ['title', 'code']
    list_filter = ['date_create', 'brush', 'cate_id', 'username']
    

class MarkAdmin(admin.ModelAdmin):
    list_display = ('mid', 'username', 'code_id_func', 'date_create')
    search_fields = ['content']
    list_filter = ['date_create', 'code_id', 'username']
    
admin.site.register(Code, CodeAdmin)
admin.site.register(Mark, MarkAdmin)