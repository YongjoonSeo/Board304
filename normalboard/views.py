from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import F

# Create your views here.
@login_required
def index(request):
    posts = Post.objects.order_by('-pk')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'normalboard/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('normalboard:detail', post.pk)
    else:
        form = PostForm()
    context = {
        'form': form,
    }
    return render(request, 'normalboard/form.html', context)

@login_required
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    commentform = CommentForm()
    comments = post.comment_set.all()
    if request.session.get('_auth_user_id'):
        cookie_name = f'hit:{request.session["_auth_user_id"]}'
    else:
        cookie_name = 'hit'
    tomorrow = datetime.replace(datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    context = {
        'post': post,
        'commentform': commentform,
        'comments': comments,
    }
    response = render(request, 'normalboard/detail.html', context)
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(post.id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{post.id}', expires=expires)
            post.hit = F('hit') + 1
            post.save()
    else:
        response.set_cookie(cookie_name, post.id, expires=expires)
        post.hit = F('hit') + 1
        post.save()
    return response

@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    data = {
        'title': post.title,
        'content': post.content,
    }
    form = PostForm(data)
    context = {
        'form': form,
        'post': post,
    }
    if request.POST.get('password') != post.password:
        messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        return redirect('normalboard:detail', post.pk)
    return render(request, 'normalboard/form.html', context)

@login_required
@require_POST
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
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'normalboard/form.html', context)

@login_required
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

@login_required
@require_POST
def create_comments(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = post
        form.save()
        messages.success(request, '댓글이 등록되었습니다.')
    else:
        messages.error(request, '내용을 입력해 주십시오.')
    return redirect('normalboard:detail', pk)

@login_required
@require_POST
def delete_comments(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('normalboard:detail', pk)

@login_required
def search(request):
    keyword = request.GET.get('query')
    posts = Post.objects.filter(title__contains=keyword).order_by('-pk')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'normalboard/index.html', context)

@login_required
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.like_users.filter(id=request.user.pk).exists():
        post.like_users.remove(request.user)
    else:
        post.like_users.add(request.user)
    return redirect('normalboard:detail', pk)