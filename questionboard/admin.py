from django.db import models
from django.contrib import admin
from .models import QPost, QComment
from martor.widgets import AdminMartorWidget

class QPostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'author', 'created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }

class QCommentAdmin(admin.ModelAdmin):
    list_display = ('qpost', 'user', 'content', 'created_at')

admin.site.register(QPost, QPostAdmin)
admin.site.register(QComment, QCommentAdmin)