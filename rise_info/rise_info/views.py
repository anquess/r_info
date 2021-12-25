from shutil import copy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.views import addTmcAuth

@login_required
def top(request):
    context = addTmcAuth({},request.user)
    return render(request, "top.html", context)

def handler404(request, exception):
    context = {"errmsg": exception}
    context = addTmcAuth(context, request.user)
    return render(request, '404.html', context, status=404)