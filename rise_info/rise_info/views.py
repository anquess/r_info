from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from rise_info.settings import TOP_PAGE_LIST_NUM
from accounts.views import addIsStaff
from infos.models import InfoRelation
from contents.models import Contents
from tech_supports.models import TechSupportsRelation


@login_required
def top(request):
    list_num = TOP_PAGE_LIST_NUM
    context = addIsStaff({}, request.user)
    infos = InfoRelation.objects.filter(
        Q(send_info__isnull=False)
    ).order_by('-updated_at')[:10]
    contents = Contents.objects.order_by('-updated_at')[:10]
    tech_supports = TechSupportsRelation.objects.filter(
        Q(send_info__isnull=False)
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
