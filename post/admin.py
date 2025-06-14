from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'creat_date', 'author_uid', 'community')
    list_filter = ('creat_date', 'community')
    search_fields = ('po_content',)