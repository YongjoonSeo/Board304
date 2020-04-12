from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Post
from .forms import PostForm

# Create your views here.
def index(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'normalboard/index.html', context)

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('normalboard:detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'normalboard/form.html', context)

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {
        'post': post,
    }
    return render(request, 'normalboard/detail.html', context)

def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = {
        'title': post.title,
        'content': post.content,
    }
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            if form.cleaned_data.get('password') == post.password:
                post = form.save()
                messages.success(request, '글 수정이 완료되었습니다.')
                return redirect('normalboard:detail', post.pk)
            else:
                messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '제출 양식이 올바르지 않습니다.')
    else:
        if request.GET.get('password') != post.password:
            messages.error(request, '글 비밀번호가 일치하지 않습니다.')
            return redirect('normalboard:detail', post.pk)
        form = PostForm(data)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'normalboard/form.html', context)

def delete(request, pk): 
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        if request.POST.get('password') == post.password:
            post.delete()
            messages.success(request, '글 삭제가 완료되었습니다.')
            return redirect('normalboard:index')
        else:
            messages.error(request, '글 비밀번호가 일치하지 않습니다.')
            return redirect('normalboard:detail', post.pk)
    context = {
        'post': post,
    }
    return render(request, 'normalboard/detail.html', context)


