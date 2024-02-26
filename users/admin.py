from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser

class CustomUserAdmin(BaseUserAdmin):
    # 定义要显示的字段列表
    list_display = ('username', 'email', 'gender', 'user_lover', 'first_name', 'last_name', 'is_staff')
    # 定义字段集，这里使用默认的即可，但你也可以自定义来包含更多字段
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('gender', 'user_lover',)}),
    )
    # 添加用户时的字段集，同样可以根据需要自定义
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ('gender', 'user_lover',)}),
    )

# 注册自定义的UserAdmin
admin.site.register(CustomUser, CustomUserAdmin)