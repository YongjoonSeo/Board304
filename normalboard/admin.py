from django.db import models
from django.contrib import admin
from .models import Post, Comment
from martor.widgets import AdminMartorWidget

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'author', 'created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)