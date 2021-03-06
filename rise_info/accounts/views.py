from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import MyPasswordChangeForm, UserAddForm
from contents.views import addMenus


def addTmcAuth(context: dict, user) -> dict:
    context['auth'] = isInTmcGroup(user)
    context = addMenus(context)
    return context


def isInTmcGroup(user) -> bool:
    try:
        tmcGroup = Group.objects.get(name="TMC")
    except:
        tmcGroup = None
    return tmcGroup in user.groups.all()


@login_required
def is_login(request):
    return HttpResponse(status=200)


@login_required
def account_new(request):
    if isInTmcGroup(request.user):
        if request.method == 'POST':
            form = UserAddForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account_list')
            else:
                messages.add_message(request, messages.WARNING, "値がおかしいです")
        else:
            context = addTmcAuth({'form': UserAddForm()}, request.user)
            return render(request, "accounts/account_new.html", context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では登録は許可されていません。")
    return redirect('account_list')


class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'accounts/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'accounts/password_change_done.html'


@login_required
def account_list(request):
    if isInTmcGroup(request.user):
        users = User.objects.all()
        context = {"users": users, }
        context = addTmcAuth(context, request.user)
        return render(request, "accounts/account_list.html", context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では登録は許可されていません。")
    return redirect('account_list')


@login_required
def account_delete(request, pk):
    if isInTmcGroup(request.user):
        user = get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        is_active_str = '有効' if user.is_active else '無効'
        messages.add_message(request, messages.INFO,
                             f"{user}の権限は、{is_active_str}になりました")

        return redirect('account_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では登録は許可されていません。")
    return redirect('account_list')
