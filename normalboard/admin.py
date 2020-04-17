from django.db import models
from django.contrib import admin
from .models import Post
from martor.widgets import AdminMartorWidget

# Register your models here.
# class PostAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'title', 'content', 'created_at', 'updated_at')

class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'content', 'created_at', 'updated_at')
    formfield_overrides = {
        models.TextField: {
            'widget': AdminMartorWidget
        },
    }

admin.site.register(Post, PostAdmin)