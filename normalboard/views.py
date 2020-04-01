from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Post

# Create your views here.
def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'normalboard/post_list.html', context)

def new_post(request):
    return render(request, 'normalboard/new_post.html')

def create_post(request):
    title = request.GET.get('title')
    password = request.GET.get('password')
    content = request.GET.get('content')
    post = Post(title=title, content=content)
    post.save()
    messages.success(request, '글 작성이 완료되었습니다.')
    return redirect(f'/community/post/{post.pk}/')

def post_detail(request, post_pk):
    post = Post.objects.get(id=post_pk)
    context = {
        'post': post,
    }
    return render(request, 'normalboard/post_detail.html', context)

def update_post(request, post_pk):
    post = Post.objects.get(id=post_pk)
    context = {
        'post': post,
    }   
    return render(request, 'normalboard/update_post.html', context)

def update_post_complete(request, post_pk):
    post = Post.objects.get(id=post_pk)
    title = request.GET.get('title')
    password = request.GET.get('password')
    content = request.GET.get('content')
    pk = request.GET.get('pk')
    if post.password == password:
        post.title = title
        post.content = content
        post.save()
        messages.success(request, '글 수정이 완료되었습니다.')
        return redirect(f'/community/post/{post.pk}/')
    else:
        messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        return redirect(f'/community/update_post/{post.pk}/')

def delete_post(request, post_pk): #추가 수정 필요 (글 비밀번호 일치하는 경우에만 삭제)
    post = Post.objects.get(id=post_pk)
    post.delete()
    return redirect('post_list')

