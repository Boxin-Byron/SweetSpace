from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Bottletext, Topic, Entry
from .forms import BottleForm, TopicForm, EntryForm

from django.utils import timezone

# Create your views here.
def index(request):
    """整个空间的主页"""
    return render(request, 'oursweetspace/index.html')


#漂流瓶
@login_required
def bottles(request):
    """显示所有已捡到且已解锁的瓶子标题"""
    now = timezone.now()
    bottles = Bottletext.objects.filter(receiver=request.user, date_unlock__lt=now).order_by('-date_added')
    context = {'bottles': bottles}
    return render(request, 'oursweetspace/bottles.html', context)


@login_required
def bottle(request, bottle_id):
    """显示瓶子内的详细信息"""
    bottle = Bottletext.objects.get(id= bottle_id)
    if bottle.receiver != request.user:
        raise Http404

    context = {'bottle': bottle}
    return render(request,'oursweetspace/bottle.html', context)


@login_required
def new_bottle(request):
    """新建漂流瓶"""
    if request.method != 'POST':
        form = BottleForm()
    else:
        #process data
        form = BottleForm(request.POST, request.FILES)
        if form.is_valid():
            new_bottle = form.save(commit= False)
            new_bottle.creator = request.user  #表单里继承了模型全部信息，在表单实现，填入模型的信息！
            if new_bottle.creator.user_lover:
                lover = new_bottle.creator.user_lover
                new_bottle.receiver = lover
            new_bottle.save()
            return redirect('oursweetspace:index')

    #显示空表单或无效
    context = {'form': form}
    return render(request,'oursweetspace/new_bottle.html', context)



#心愿单
@login_required
def topics(request):
    """显示当前用户及其配对用户的所有主题"""
    user_topics = Topic.objects.filter(owner=request.user)
    if request.user.user_lover:
        lover = request.user.user_lover
        lover_topics = Topic.objects.filter(owner=lover)
        user_topics |= lover_topics  # 使用 | 运算符合并两个查询集

    topics = user_topics.order_by("date_added")
    context = {'usertopics': topics}
    return render(request, 'oursweetspace/topics.html', context)



@login_required
def topic(request, topic_id):
    """显示某一主题，及内部所有条目"""
    topic = Topic.objects.get(id= topic_id)
    # 确认该topic属于该用户或其lover
    if topic.owner != request.user and topic.owner !=request.user.user_lover:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'usertopic': topic, 'userentries': entries}
    return render(request, 'oursweetspace/topic.html', context) 


@login_required
def new_topic(request):
    """用户添加新主题"""
    if request.method != 'POST':
        #未提交数据：创建新表单
        form = TopicForm()
    else:
        #POST提交的数据：对数据进行处理
        form = TopicForm(data= request.POST)
        if form.is_valid():
            new_topic = form.save(commit= False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('oursweetspace:topics')

    #显示空表单/指出数据无效
    context = {'form': form}
    return render(request,'oursweetspace/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定主题中添加条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user and topic.owner !=request.user.user_lover:
        raise Http404

    if request.method != 'POST':
        #no data    
        form = EntryForm()
    else:
        #data processing
        form = EntryForm(data= request.POST)
        if form.is_valid():
            new_entry = form.save(commit= False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('oursweetspace:topic',topic_id = topic_id)

    #显示空表单或指出表单数据无效
    context = {'topic': topic, 'form': form}
    return render(request,'oursweetspace/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user and topic.owner !=request.user.user_lover:
        raise Http404

    if request.method != 'POST':
        #初次请求：使用当前条目？？？
        form = EntryForm(instance= entry)
    else:
        #process POST提交的数据  
        form = EntryForm(instance= entry, data= request.POST)
        if form.is_valid():
            form.save()
            return redirect('oursweetspace:topic', topic_id= topic.id)#没关系 后面的topic是类

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'oursweetspace/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user and topic.owner !=request.user.user_lover:
        raise Http404
    
    # 确保请求方法是POST，以避免非法请求
    if request.method == 'POST':
        entry.delete()
        return redirect('oursweetspace:topic', topic_id = topic.id)  # 重定向到一个视图，例如条目列表
    else:
        # 如果不是POST请求，可以重定向或显示一个错误页面
        return redirect('oursweetspace:topic')