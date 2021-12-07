from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm


def login(request):
    title = 'Вход'
    form_name = 'Вход в систему'
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))

    context = {
        'form_name': form_name,
        'title': title,
        'login_form': login_form
    }

    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit(request):
    title = 'Профиль'
    form_name = 'Настройка профилья'
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('authapp:edit'))

    else:
        edit_form = ShopUserEditForm(instance=request.user)
    context = {
        'form_name': form_name,
        'title': title,
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', context)


def register(request):
    title = 'Регистрация'
    form_name = 'Регистрация'
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            return HttpResponseRedirect(reverse('authapp:login'))

    else:
        register_form = ShopUserRegisterForm()
    context = {
        'form_name': form_name,
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)
