from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def top(request):
    return render(request, "top.html")

def handler404(request, exception):
    context = {"msg": exception}
    return render(request, '404.html', context, status=404)