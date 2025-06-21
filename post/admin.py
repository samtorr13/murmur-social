from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Post
from comments.models import Comment
from reports.models import Report

class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('global_pid', 'co_content', 'creat_date', 'anon')
    can_delete = False
    readonly_fields = ('global_pid', 'co_content', 'creat_date', 'anon')
    show_change_link = True




@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('global_pid', 'creat_date', 'author', 'community')
    readonly_fields = ('global_pid', 'creat_date', 'author', 'po_content')
    list_filter = ('creat_date', 'community')
    search_fields = ('po_content',)
    inlines = (CommentInLine,)
    exclude = ('global_pid',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('global_pid', 'creat_date', 'author', 'parent')
    list_filter = ('creat_date',)
    search_fields = ('com_cont',)
    inlines = (CommentInLine,)
    exclude = ('global_pid',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('global_pid', 'status', 'moderator', 'get_content_object')
    readonly_fields = ('global_pid', 'get_content_object', 'content_type', 'reason')
    exclude = ('object_id',)
    list_filter = ('status',)
    search_fields = ('review_notes',)

    def get_content_object(self, obj):
        pid = obj.global_pid
        post = Post.objects.filter(global_pid=pid).first()
        if post:
            url = reverse("admin:post_post_change", args=[post.pk])
            return format_html('<a href="{}">Post: {}</a>', url, post.po_content[:30])

        comment = Comment.objects.filter(global_pid=pid).first()
        if comment:
            url = reverse("admin:comment_comment_change", args=[comment.pk])
            return format_html('<a href="{}">Comment: {}</a>', url, comment.co_content[:30])

        return "No encontrado"

    get_content_object.short_description = "Contenido reportado"
#admin.site.register(Comment)