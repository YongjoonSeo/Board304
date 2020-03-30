from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Student

# Register your models here.
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    
class UserAdmin(BaseUserAdmin):
    inlines = (StudentInline,)
    list_display = ('username', 'get_number', 'email', 'last_name', 'first_name', 'is_staff')
    list_select_relates = ('student',)

    def get_number(self, instance):
        return instance.student.number
    get_number.short_description = '학번'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)