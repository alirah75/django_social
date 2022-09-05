from django.contrib import admin
from.models import Post, Comment, Like

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'slug', 'updated']
    search_fields = ['body', 'slug']
    list_filter = ['updated']
    prepopulated_fields = {'slug': ['body']}
    raw_id_fields = ['user']

# admin.site.register(Post)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created', 'is_reply']
    raw_id_fields = ['user', 'post', 'reply']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']
