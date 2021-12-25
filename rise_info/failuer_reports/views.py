from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import FailuerReport
from accounts.views import addTmcAuth

@login_required
def failuer_report_list(request):
    infos = FailuerReport.objects.all()
    context = {'infos':infos}
    context = addTmcAuth(context, request.user)
    return render(request, "failuer_reports/list.html", context)    

