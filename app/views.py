from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Like, Follow, User
from .forms import PostForm

#用户认证（注册与登录）
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'login.html', {'form': form})

#核心展示（Feed 流）
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#内容发布（发帖）
@login_required
def feed(request):
    # 获取我关注的人的 ID 列表 [cite: 209]
    following = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
    # 筛选出关注人的帖子 + 自己的帖子 [cite: 210]
    posts = Post.objects.filter(author__in=following) | Post.objects.filter(author=request.user)
    posts = posts.distinct().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

#社交交互（点赞与关注）
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # 必须包含 request.FILES 以处理图片 [cite: 216]
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user # 自动将作者设为当前登录用户 [cite: 219]
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})
