from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import MyPasswordChangeForm, UserAddForm, UserMailConfigForm
from .models import User_mail_config


def addIsStaff(context: dict, user) -> dict:
    from contents.views import addMenus
    context['auth'] = user.is_staff
    context = addMenus(context)
    return context


@login_required
def is_login(request):
    return HttpResponse(status=200)


@login_required
def account_new(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = UserAddForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account_list')
            else:
                messages.add_message(request, messages.WARNING, "値がおかしいです")
        else:
            context = addIsStaff({'form': UserAddForm()}, request.user)
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
    if request.user.is_staff:
        users = User.objects.all()
        context = {"users": users, }
        context = addIsStaff(context, request.user)
        return render(request, "accounts/account_list.html", context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では登録は許可されていません。")
    return redirect('account_list')


@login_required
def account_delete(request, pk):
    if request.user.is_staff:
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


@login_required
def edit_user_mail_config(request):
    user_mail_config = User_mail_config.objects.get_or_none(user=request.user)
    form = UserMailConfigForm(request.POST or None, instance=user_mail_config)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO,
                             "%sアカウントのメール設定が更新されました" % request.user)
        return redirect('top')
    else:
        context = addIsStaff(
            {
                'form': form,
                'pk': request.user,
            },
            request.user)
        return render(request, 'accounts/edit_user_mail_config.html', context)
