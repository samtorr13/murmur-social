from django.contrib import admin
from .models import Post
from comments.models import Comment
from comments.models import Comment
class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('global_uid', 'co_content', 'creat_date', 'anon')
    can_delete = False
    readonly_fields = ('global_uid', 'co_content', 'creat_date', 'anon')
    show_change_link = True

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('global_uid', 'creat_date', 'author', 'community')
    list_filter = ('creat_date', 'community')
    search_fields = ('po_content',)
    inlines = (CommentInLine,)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('global_uid', 'creat_date', 'author')
    list_filter = ('creat_date',)
    search_fields = ('com_cont',)
    inlines = (CommentInLine,)
#admin.site.register(Comment)