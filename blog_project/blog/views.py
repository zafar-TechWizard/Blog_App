from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, SignUpForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        posts = Post.objects.all()
    else:
        user_post = Post.objects.filter(author = request.user, status=Post.APPROVED)
    return render(request, 'dashboard.html', {'posts': posts if request.user.is_superuser else user_post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = Post.PENDING
            form.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save(commit=False)
            post_author = request.user
            post_status = request.PENDING
            post.save
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'post_confirm_delete.html', {'post': post})

def post_list(request):
    posts = Post.objects.filter(status=Post.APPROVED) #get all post from db
    return render(request, 'post_list.html', {'posts': posts})


@staff_member_required
def post_review_list(request):
    posts = Post.objects.filter(status=Post.PENDING)
    return render(request, 'post_review_list.html', {'Post': posts})


@staff_member_required
def post_review(request, pk, action):
    post = get_object_or_404(Post, pk=pk)
    if action == 'approve':
        post.status = Post.REJECTED

    elif action == 'reject':
        post.status = Post.REJECTED
        post.delete()
    
    post.save()

    return redirect('post_review_list')