from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages

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
        return render(request, 'login.html')

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')