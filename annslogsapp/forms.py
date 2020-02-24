#!/usr/bin/python
# -*- coding:utf-8 -*-
#@Author : jiaoxiao.lan
#@File   : forms.py

from django import forms
from .models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name',]
        # 让 Django 不要为字段 name 生成标签
        labels = {'name': ''}

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['name']
        labels = {'name': ''}
        # 设置属性widgets，可覆盖Django选择的默认小部件
        # 文本区域改成80列（非默认的40列）
        widgets = {'name': forms.Textarea(attrs={'cols': 80})}
