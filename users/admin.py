from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from post.models import Post  # Importá también el modelo Comment
from comments.models import Comment
class PostInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('global_uid','po_content', 'creat_date', 'anon')
    readonly_fields = ('global_uid','po_content', 'creat_date', 'anon')
    show_change_link = True

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('global_uid','co_content', 'creat_date', 'anon')
    readonly_fields = ('global_uid','co_content', 'creat_date', 'anon')
    show_change_link = True

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    inlines = [PostInline, CommentInline]

    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}),
    )

    search_fields = ('username', 'email')
    ordering = ('id',)
