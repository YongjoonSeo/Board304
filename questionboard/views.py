from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import QPost, QComment
from .forms import QPostForm, QCommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import F

# Create your views here.
@login_required
def index(request):
    qposts = QPost.objects.order_by('-pk')
    paginator = Paginator(qposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'questionboard/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = QPostForm(request.POST)
        if form.is_valid():
            qpost = form.save(commit=False)
            qpost.author = request.user
            qpost.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('questionboard:detail', qpost.pk)
    else:
        form = QPostForm()
    context = {
        'form': form,
    }
    return render(request, 'questionboard/form.html', context)

@login_required
def detail(request, pk):
    qpost = get_object_or_404(QPost, pk=pk)
    commentform = QCommentForm()
    comments = qpost.qcomment_set.all()
    if request.session.get('_auth_user_id'):
        cookie_name = f'hit:{request.session["_auth_user_id"]}'
    else:
        cookie_name = 'hit'
    tomorrow = datetime.replace(datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    context = {
        'qpost': qpost,
        'commentform': commentform,
        'comments': comments,
    }
    response = render(request, 'questionboard/detail.html', context)
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(qpost.id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{qpost.id}', expires=expires)
            qpost.hit = F('hit') + 1
            qpost.save()
    else:
        response.set_cookie(cookie_name, qpost.id, expires=expires)
        qpost.hit = F('hit') + 1
        qpost.save()
    return response

@login_required
def edit(request, pk):
    qpost = get_object_or_404(QPost, pk=pk)
    data = {
        'title': qpost.title,
        'content': qpost.content,
    }
    form = QPostForm(data)
    context = {
        'form': form,
        'qpost': qpost,
    }
    if request.POST.get('password') != qpost.password:
        messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        return redirect('questionboard:detail', qpost.pk)
    return render(request, 'questionboard/form.html', context)

@login_required
@require_POST
def update(request, pk):
    qpost = get_object_or_404(QPost, pk=pk)
    data = {
        'title': qpost.title,
        'content': qpost.content,
    }
    if request.method == 'POST':
        form = QPostForm(request.POST, instance=qpost)
        if form.is_valid():
            if form.cleaned_data.get('password') == qpost.password:
                qpost = form.save()
                messages.success(request, '글 수정이 완료되었습니다.')
                return redirect('questionboard:detail', qpost.pk)
            else:
                messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '제출 양식이 올바르지 않습니다.')
    context = {
        'form': form,
        'qpost': qpost,
    }
    return render(request, 'questionboard/form.html', context)

@login_required
def delete(request, pk): 
    qpost = get_object_or_404(QPost, pk=pk)
    if request.method == 'POST':
        if request.POST.get('password') == qpost.password:
            qpost.delete()
            messages.success(request, '글 삭제가 완료되었습니다.')
            return redirect('questionboard:index')
        else:
            messages.error(request, '글 비밀번호가 일치하지 않습니다.')
            return redirect('questionboard:detail', qpost.pk)
    context = {
        'qpost': qpost,
    }
    return render(request, 'questionboard/detail.html', context)

@login_required
@require_POST
def create_comments(request, pk):
    qpost = get_object_or_404(QPost, pk=pk)
    form = QCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.qpost = qpost
        form.save()
        messages.success(request, '댓글이 등록되었습니다.')
    else:
        messages.error(request, '내용을 입력해 주십시오.')
    return redirect('questionboard:detail', pk)

@login_required
@require_POST
def delete_comments(request, pk, comment_pk):
    comment = get_object_or_404(QComment, pk=comment_pk)
    comment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('questionboard:detail', pk)

@login_required
def search(request):
    keyword = request.GET.get('query')
    qposts = QPost.objects.filter(title__contains=keyword).order_by('-pk')
    paginator = Paginator(qposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'questionboard/index.html', context)

@login_required
def like(request, pk):
    qpost = get_object_or_404(QPost, pk=pk)
    if qpost.like_users.filter(id=request.user.pk).exists():
        qpost.like_users.remove(request.user)
    else:
        qpost.like_users.add(request.user)
    return redirect('questionboard:detail', pk)