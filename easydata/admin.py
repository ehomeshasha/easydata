from django.contrib import admin

from easydata.category.models import category

class categoryAdmin(admin.ModelAdmin):
    list_display = ('cid', 'name','description','ctype', 'status')
    search_fields = ['name', 'description']
    list_filter = ['ctype', 'status']
    

admin.site.register(category, categoryAdmin)
