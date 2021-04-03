from django.contrib import admin

from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    #
    # def formatted_hit_count(self, obj):
    #     return obj.current_hit_count if obj.current_hit_count > 0 else '-'
    #
    # formatted_hit_count.admin_order_field = 'hit_count'
    # formatted_hit_count.short_description = 'Hits'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'publish', 'active', 'author')
    list_filter = ('active', 'publish',)
    search_fields = ('body',)
