from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import render

def isInTmcGroup(user) -> bool:
    try:
        tmcGroup = Group.objects.get(name="TMC")
    except:
        tmcGroup = None
    return tmcGroup in user.groups.all()

def isRoot(user) -> bool:
    return user.username == "root" 

@login_required
def sign_up(request):
    if isRoot(request.user):
        form = UserCreationForm()
        return render(request, "accounts/signup.html", {'form': form})
    else:
        return HttpResponseForbidden("この権限では登録は許可されていません。")
