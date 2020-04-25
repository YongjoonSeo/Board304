from django.db import models
from django.contrib import admin
from .models import CodePost, CodeComment
from martor.widgets import AdminMartorWidget

class CodePostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'author', 'created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }

class CodeCommentAdmin(admin.ModelAdmin):
    list_display = ('codepost', 'user', 'content', 'created_at')

admin.site.register(CodePost, CodePostAdmin)
admin.site.register(CodeComment, CodeCommentAdmin)