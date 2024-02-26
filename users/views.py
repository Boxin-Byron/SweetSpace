from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

"""
def register(request):
    #注册新用户，成功则自动登录
    if request.method != 'POST':
        # 显示空注册表单
        form = UserCreationForm()
    else:
        #处理已填写的表单
        form = UserCreationForm(data= request.POST)

        if form.is_valid():
            new_user = form.save()
            #登录并回到主页
            login(request, new_user)
            return redirect('oursweetspace:index')

    #显示空表单/表单无效
    context = {'form': form}
    return render(request, 'registration/register.html', context)
"""

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_lover = form.cleaned_data.get('user_lover')
            if user_lover:
                user_lover.user_lover = user
                user_lover.save()
            login(request, user)
            return redirect('oursweetspace:index')  # Assuming you have a login view
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """login"""
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        next_url = request.GET.get('next', '/')
        return redirect(next_url)
    else:
        return redirect('users:login') #这里users会自动定位到html文件   

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('users:logged_out')
    #防止用户手动输入url引发GET，或其他错误！！
    return redirect('oursweetspace:index')

def logged_out(request):
    return render('users/logged_out.html')#也可以手动