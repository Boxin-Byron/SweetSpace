"""为应用users定义url模式"""

from django.urls import path, include

from . import views

app_name = 'users'
urlpatterns = [
	# 包含django默认身份验证url
	path('', include('django.contrib.auth.urls')),
	# 用户注册
	path('register/', views.register, name= 'register'),
	# 登录
	path('login/', views.login_view, name= 'login'),
	# 注销
	path('logout/', views.logout_view, name= 'logout'),
	# 注销成功 回到首页
	path('logged_out/', views.logged_out, name='logged_out'),
]