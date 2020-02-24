"""annslogsapp URL Configuration
这里定义app的URL模式
"""
from django.urls import path
from annslogsapp import views

app_name = 'annslogsapp'
urlpatterns = [
    # 主页
    path('', views.index, name='index'),
    #Topic
    path('topics/', views.topics, name='topics'),
    #Topic的细节
    path('topic/<topic_id>/',  views.topic, name='topic'),

    # 用于添加新主题的网页
    path('new_topic/', views.new_topic, name='new_topic'),

    # 用于添加主题新条目的网页
    path('new_entry/<topic_id>/', views.new_entry, name='new_entry'),
    # 用于主题条目编辑的网页
    path('edit_entry/<entry_id>/', views.edit_entry, name='edit_entry'),
]
