from django.contrib import admin
from sorl.thumbnail.admin import AdminImageMixin

from .models import Post, Comment, Author


@admin.register(Post)
class PostAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'publish', 'active', 'author')
    list_filter = ('active', 'publish',)
    search_fields = ('body',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass