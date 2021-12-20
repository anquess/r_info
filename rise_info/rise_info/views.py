from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def top(request):
    return render(request, "top.html")

def handler400(request, exception):
    return render(request, '400.html', {}, status=400)