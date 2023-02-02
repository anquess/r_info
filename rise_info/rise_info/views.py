from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rise_info.settings import TOP_PAGE_LIST_NUM
from accounts.views import addIsStaff
from infos.models import Info
from contents.models import Contents
from tech_supports.models import TechSupports
from rise_info.choices import RegisterStatusChoices, RegisterStatusChoicesSupo


@login_required
def top(request):
    list_num = TOP_PAGE_LIST_NUM
    context = addIsStaff({}, request.user)
    infos = Info.objects.filter(
        Q(select_register=RegisterStatusChoices.REGISTER)
    ).order_by('-updated_at')[:10]
    contents = Contents.objects.filter(
        Q(select_register=RegisterStatusChoices.REGISTER)
    ).order_by('-updated_at')[:10]
    tech_supports = TechSupports.objects.filter(
        Q(select_register=RegisterStatusChoices.REGISTER)
    ).order_by('-updated_at')[:10]
    context['list_num'] = list_num
    context['infos'] = infos
    context['contents'] = contents
    context['tech_supports'] = tech_supports
    return render(request, "top.html", context)


def handler404(request, exception):
    context = {"errmsg": exception}
    context = addIsStaff(context, request.user)
    return render(request, '404.html', context, status=404)
