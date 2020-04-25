from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Student

# Create your views here.

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if not username:
            messages.error(request, '아이디는 필수값입니다.')
        elif not password:
            messages.error(request, '비밀번호는 필수값입니다.')
        elif user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, '가입하지 않은 아이디이거나, 잘못된 비밀번호입니다.')
        return render(request, 'accounts/login.html')
    
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, '비밀번호가 변경되었습니다.')
            return redirect('home')
        else:
            messages.error(request, '부적합한 비밀번호이거나 비밀번호가 일치하지 않습니다.')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/change_password.html', context)

