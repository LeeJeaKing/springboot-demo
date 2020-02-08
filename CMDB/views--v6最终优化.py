from django.shortcuts import render,redirect,reverse

# Create your views here.

from .models import User
from .validators import UserValiator

def index(request):
    if  not request.session.get('user'):
        return redirect('User:login')
    return render(request,'user/index.html',{'users':User.get_list()}) #返回对象，直接给前端，前端可直接调用

def login(request):
    if request.method == 'GET':
        return render(request,'user/login.html')
    else:
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = UserValiator.valid_login(name,password) #调用User函数的登录方法

        if user:
            request.session['user'] = user.as_dict() #如果存在用户，则调用保存成字典
            return redirect('User:index')
        else:
            return render(request,'user/login.html',{'name':name,'error':{'defalut':"用户名或密码错误"}})


def logout(request):
    request.session.flush()
    return redirect('User:login')


def delete(request):
    if not request.session.get('user'):
        return redirect('User:login')
    uid = request.GET.get('uid')
    User.delete_by_id(uid)

    return redirect('User:index')


def view(request):
    if not request.session.get('user'):
        return redirect('User:login')
    uid = request.GET.get('uid')
    return render(request,'user/view.html',{'user':User.get_by_id(uid)})


def update(request):
    if not request.session.get('user'):
        return redirect('User:login')

    is_valid,user,errors = UserValiator.valid_update(request.POST)
    if is_valid:
        user.update()
        return redirect('User:index')
    else:
        return render(request,'user/view.html',{'user':user,'errors':errors})


def create(request):
    if not request.session.get('user'):
        return redirect('User:login')

    if request.method == 'GET':
        return render(request,'user/create.html')
    else:
        is_valid, user, errors = UserValiator.valid_create(request.POST)
        if is_valid:
            User.create(user)
            return redirect('User:index')
        else:
            return render(request,'user/create.html',{'user':user,'errors':errors})