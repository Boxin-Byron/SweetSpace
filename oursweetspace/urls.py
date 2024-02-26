"""定义URL模式"""

from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'oursweetspace'
urlpatterns = [
    #主页
    path('', views.index, name= 'index'),
    
    #漂流瓶

    # 显示已功能介绍、以及拾起的对方的漂流瓶概览
    path('drift_bottles/', views.bottles, name= 'bottles'),
    # 显示某个漂流瓶的细节内容
    path('drift_bottles/<int:bottle_id>',views.bottle, name= 'bottle'),
    # 用于新建漂流瓶
    path('new_bottle/',views.new_bottle, name= 'new_bottle'),
    
    #心愿单

    # 显示所有主题
    path('lists/', views.topics, name='topics'),
    # 某一主题的详细页面内容
    path('lists/<int:topic_id>/', views.topic, name='topic'),
    # 用于添加新主题的页面
    path('new_topic/', views.new_topic, name='new_topic'),
    # 用于添加新条目的页面
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    # 用于编辑entry的页面
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # 用于删除entry
    path('delete_entry/<int:entry_id>/', views.delete_entry, name="delete_entry"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)