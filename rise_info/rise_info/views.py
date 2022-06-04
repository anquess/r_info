import imp
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from datetime import datetime
from dateutil.relativedelta import relativedelta

from accounts.views import addTmcAuth
from infos.models import Info
from contents.models import Contents


@login_required
def top(request):
    context = addTmcAuth({}, request.user)
#    ip = request.META.get('REMOTE_ADDR') # django toolbar
#    context["IP"] = ip # django toolbar
    info = Info.objects.filter(is_disclosed=True).filter(
        disclosure_date__lte=datetime.today()).filter(
        disclosure_date__gte=datetime.today() - relativedelta(months=24)).order_by('-disclosure_date')
    contents = Contents.objects.filter(updated_at__gte=datetime.today(
    ) - relativedelta(months=3)).order_by('-updated_at')
    context['infos'] = info
    context['contents'] = contents
    return render(request, "top.html", context)


def handler404(request, exception):
    context = {"errmsg": exception}
    context = addTmcAuth(context, request.user)
    return render(request, '404.html', context, status=404)
