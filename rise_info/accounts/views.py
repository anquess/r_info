from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import MyPasswordChangeForm, UserAddForm

def isInTmcGroup(user) -> bool:
    try:
        tmcGroup = Group.objects.get(name="TMC")
    except:
        tmcGroup = None
    return tmcGroup in user.groups.all()

def isRoot(user) -> bool:
    return user.username == "root" 

@login_required
def account_new(request):
    if isRoot(request.user):
        if request.method == 'POST':
            form = UserAddForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('account_list')
            else:
                return HttpResponse("invalid request", status=400)
        else:
            form = UserAddForm()
            return render(request, "accounts/account_new.html", {'form': form})
    else:
        return HttpResponseForbidden("この権限では登録は許可されていません。")

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
    if isRoot(request.user):
        users = User.objects.all()
        context = { "users": users, }
        return render(request, "accounts/account_list.html", context)
    else:
        return HttpResponseForbidden("この権限では登録は許可されていません。")

@login_required
def account_delete(request, pk):
    if isRoot(request.user):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('account_list')
    else:
        return HttpResponseForbidden("この権限では登録は許可されていません。")
