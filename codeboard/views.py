from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import CodePost, CodeComment
from .forms import CodePostForm, CodeCommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import F

# Create your views here.
@login_required
def index(request):
    codeposts = CodePost.objects.order_by('-pk')
    paginator = Paginator(codeposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'codeboard/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = CodePostForm(request.POST)
        if form.is_valid():
            codepost = form.save(commit=False)
            codepost.author = request.user
            codepost.save()
            messages.success(request, '글 작성이 완료되었습니다.')
            return redirect('codeboard:detail', codepost.pk)
        messages.warning(request, '글 제목은 20자 이내, 비밀번호는 8자 이내입니다.')
    else:
        form = CodePostForm()
    context = {
        'form': form,
    }
    return render(request, 'codeboard/form.html', context)

@login_required
def detail(request, pk):
    codepost = get_object_or_404(CodePost, pk=pk)
    codecommentform = CodeCommentForm()
    comments = codepost.codecomment_set.all()
    if request.session.get('_auth_user_id'):
        cookie_name = f'hit:{request.session["_auth_user_id"]}'
    else:
        cookie_name = 'hit'
    tomorrow = datetime.replace(datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    context = {
        'codepost': codepost,
        'codecommentform': codecommentform,
        'comments': comments,
    }
    response = render(request, 'codeboard/detail.html', context)
    if request.COOKIES.get(cookie_name) is not None:
        cookies = request.COOKIES.get(cookie_name)
        cookies_list = cookies.split('|')
        if str(codepost.id) not in cookies_list:
            response.set_cookie(cookie_name, cookies + f'|{codepost.id}', expires=expires)
            codepost.hit = F('hit') + 1
            codepost.save()
    else:
        response.set_cookie(cookie_name, codepost.id, expires=expires)
        codepost.hit = F('hit') + 1
        codepost.save()
    return response

@login_required
def edit(request, pk):
    codepost = get_object_or_404(CodePost, pk=pk)
    data = {
        'title': codepost.title,
        'content': codepost.content,
    }
    form = CodePostForm(data)
    context = {
        'form': form,
        'codepost': codepost,
    }
    if request.POST.get('password') != codepost.password:
        messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        return redirect('codeboard:detail', codepost.pk)
    return render(request, 'codeboard/form.html', context)

@login_required
@require_POST
def update(request, pk):
    codepost = get_object_or_404(CodePost, pk=pk)
    data = {
        'title': codepost.title,
        'content': codepost.content,
    }
    if request.method == 'POST':
        form = CodePostForm(request.POST, instance=codepost)
        if form.is_valid():
            if form.cleaned_data.get('password') == codepost.password:
                codepost = form.save()
                messages.success(request, '글 수정이 완료되었습니다.')
                return redirect('codeboard:detail', codepost.pk)
            else:
                messages.error(request, '글 비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '제출 양식이 올바르지 않습니다.')
    context = {
        'form': form,
        'codepost': codepost,
    }
    return render(request, 'codeboard/form.html', context)

@login_required
def delete(request, pk): 
    codepost = get_object_or_404(CodePost, pk=pk)
    if request.method == 'POST':
        if request.POST.get('password') == codepost.password:
            codepost.delete()
            messages.success(request, '글 삭제가 완료되었습니다.')
            return redirect('codeboard:index')
        else:
            messages.error(request, '글 비밀번호가 일치하지 않습니다.')
            return redirect('codeboard:detail', codepost.pk)
    context = {
        'codepost': codepost,
    }
    return render(request, 'codeboard/detail.html', context)

@login_required
@require_POST
def create_comments(request, pk):
    codepost = get_object_or_404(CodePost, pk=pk)
    form = CodeCommentForm(request.POST)
    if form.is_valid():
        codecomment = form.save(commit=False)
        codecomment.user = request.user
        codecomment.codepost = codepost
        form.save()
        messages.success(request, '댓글이 등록되었습니다.')
    else:
        messages.error(request, '내용을 입력해 주십시오.')
    return redirect('codeboard:detail', pk)

@login_required
@require_POST
def delete_comments(request, pk, comment_pk):
    codecomment = get_object_or_404(CodeComment, pk=comment_pk)
    codecomment.delete()
    messages.success(request, '댓글이 삭제되었습니다.')
    return redirect('codeboard:detail', pk)

@login_required
def search(request):
    keyword = request.GET.get('query')
    codeposts = CodePost.objects.filter(title__contains=keyword).order_by('-pk')
    paginator = Paginator(codeposts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'codeboard/index.html', context)

@login_required
def like(request, pk):
    codepost = get_object_or_404(CodePost, pk=pk)
    if codepost.like_users.filter(id=request.user.pk).exists():
        codepost.like_users.remove(request.user)
    else:
        codepost.like_users.add(request.user)
    return redirect('codeboard:detail', pk)