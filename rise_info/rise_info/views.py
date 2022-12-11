from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from datetime import datetime
from dateutil.relativedelta import relativedelta

from rise_info.settings import TOP_PAGE_LIST_NUM
from accounts.views import addTmcAuth
from infos.models import Info
from contents.models import Contents
from tech_supports.models import TechSupports


@login_required
def top(request):
    list_num = TOP_PAGE_LIST_NUM
    context = addTmcAuth({}, request.user)
    # ip = request.META.get('REMOTE_ADDR') # django toolbar
    # context["IP"] = ip # django toolbar
    infos = Info.objects.filter(
        Q(select_register='under_renewal') |
        Q(select_register='register'),
    ).order_by('-updated_at')[:10]
    contents = Contents.objects.order_by('-updated_at')[:10]
    tech_supports = TechSupports.objects.order_by('-updated_at')[:10]
    context['list_num'] = list_num
    context['infos'] = infos
    context['contents'] = contents
    context['tech_supports'] = tech_supports
    return render(request, "top.html", context)


def handler404(request, exception):
    context = {"errmsg": exception}
    context = addTmcAuth(context, request.user)
    return render(request, '404.html', context, status=404)
