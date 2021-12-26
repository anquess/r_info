from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .models import FailuerReport
from .forms import FailuerReportForm
from accounts.views import addTmcAuth

@login_required
def failuer_report_list(request):
    infos = FailuerReport.objects.all()
    context = {
        'infos':infos,
        'user':request.user
        }
    context = addTmcAuth(context, request.user)
    return render(request, "failuer_reports/list.html", context)    

@login_required
def failuer_report_new(request):
    if request.method == 'POST':
        form = FailuerReportForm(request.POST)
        if form.is_valid():
            info = form.save(commit=False)
            info.created_by = request.user
            info.save()
            return redirect('failuer_report_list')
        else:
            raise Http404(form.errors)
    else:
        form = FailuerReportForm()
        context = addTmcAuth({'form': form}, request.user)
    return render(request, "failuer_reports/new.html", context)

@login_required
def failuer_report_edit(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    if info:
        if request.method == "POST":
            form = FailuerReportForm(request.POST, instance=info)
            if form.is_valid():
                form.save()
                return redirect('failuer_report_list')
            else:
                raise Http404('値がおかしい')
        else:
            form = FailuerReportForm(instance=info)
        return render(request, 'failuer_reports/edit.html', {'form': form })

    else:
        raise Http404("このデータがありません")

@login_required
def failuer_report_detail(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    if info:
        context ={
            'info': info,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'failuer_reports/detail.html', context)
    else:
        raise Http404('該当Infoはありません。')

@login_required
def failuer_report_del(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    if info:
        title = info.title
        info.delete()
        return redirect('failuer_report_list')
    else:
        raise Http404('該当Infoは既に削除されてありません。')
