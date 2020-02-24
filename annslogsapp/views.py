from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Topic
from .forms import TopicForm, EntryForm, Entry

# Create your views here.
def index(request):
    return render(request, 'annslogsapp/index.html')


""" 将login_required()作为装饰器 """
# 在访问topics（）之前要先调用login_required()
@login_required()
def topics(request):

    # 仅显示主题名称
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'annslogsapp/topics.html', context)


""" 显示单个主题及其所有条目 """
@login_required()
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic, request)

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'annslogsapp/topic.html', context)


"""创建新主题"""
@login_required()
def new_topic(request):
    # 添加新主题
    if request.method != 'POST':
        form = TopicForm()
    else:
        # 对POST提交的数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            # 将新建的主题关联到当前登录的账号
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('annslogsapp:topics'))
    context = {'form': form}
    return render(request, 'annslogsapp/new_topic.html', context)


""" 在子主题下添加内容 """
@login_required()
def new_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)

    check_topic_owner(topic, request)

    if request.method != 'POST':
        # 未提交数据 , 创建一个空表单
        form = EntryForm()
    else:
        # POST 提交的数据 , 对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # 传递了实参commit=False，让Django创建一个新的配料对象，并将其存储到new_topping中，但不将它保存到数据库中
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            # 把配料保存到数据库，并将其与正确的披萨相关联
            new_entry.save()
            return HttpResponseRedirect(reverse('annslogsapp:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}
    return render(request, 'annslogsapp/new_entry.html', context)


""" 编辑既有条目 """
@login_required()
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    check_topic_owner(topic, request)

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST 提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('annslogsapp:topic', args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'annslogsapp/edit_entry.html', context)

def check_topic_owner(topic, request):
    """校验关联到的用户是否为当前登录的用户"""
    if topic.owner != request.user:
        raise Http404
