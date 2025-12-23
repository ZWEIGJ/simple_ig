from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
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

#核心展示（Feed 流）
@login_required
def feed(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)
    
    # 因为上面直接导入了 Q，所以这里不需要写 models.Q，直接写 Q 即可
    posts = Post.objects.filter(
        Q(author_id__in=following_ids) | Q(author=request.user)
    ).order_by('-created_at')
    
    return render(request, 'feed.html', {
        'posts': posts,
        'following_ids': following_ids
    })

#内容发布（发帖）
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

#社交交互（点赞与关注）
@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete() # 如果已经点过赞，则取消 [cite: 230]
    return redirect('feed')

@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.user != target_user:
        follow, created = Follow.objects.get_or_create(follower=request.user, followed=target_user)
        if not created:
            follow.delete()
    
    # 修改这里：尝试跳回之前的页面，如果没有来源则回首页
    return redirect(request.META.get('HTTP_REFERER', 'feed'))

#个人主页
@login_required
def profile(request, username):
    user_profile = get_object_or_404(User, username=username)
    user_posts = Post.objects.filter(author=user_profile).order_by('-created_at')
    
    # 获取当前用户的关注列表，用于判断按钮状态
    following_ids = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)
    
    context = {
        'user_profile': user_profile,
        'user_posts': user_posts,
        'posts_count': user_posts.count(),
        # 修复报错：改回 .followers (Django 默认名称)
        'followers_count': user_profile.followers.count(), 
        'following_count': user_profile.following.count(),
        'following_ids': following_ids,
    }
    return render(request, 'profile.html', context)

#探索广场
@login_required
def explore(request):
    all_posts = Post.objects.all().order_by('-created_at')
    # 获取当前用户所有关注的人的 ID 列表
    following_ids = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)
    return render(request, 'explore.html', {
        'posts': all_posts,
        'following_ids': following_ids # 传给前端
    })