from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import Http404

from .models import FailuerReport, AttachmentFile
from .forms import FailuerReportForm, FileFormSet
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
    form = FailuerReportForm(request.POST or None)
    context = addTmcAuth({'form': form}, request.user)
    if request.method == "POST" and form.is_valid():
        info = form.save(commit=False)
        formset = FileFormSet(request.POST, request.FILES, instance=info)
        if formset.is_valid():
            info.created_by = request.user
            info.save()
            formset.save()
            messages.add_message(request, messages.INFO, '更新されました。')
            return redirect('failuer_report_list')
        else:
            context['formset'] = formset
    else:
        context['formset'] = FileFormSet()
    return render(request, "failuer_reports/new.html", context)

@login_required
def failuer_report_edit(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    if info:
        if info.created_by==request.user:
            form = FailuerReportForm(request.POST or None, files=request.FILES or None, instance=info)
            formset = FileFormSet(request.POST or None, files=request.FILES or None, instance=info)
            if (request.method == "POST" and form.is_valid()) :
                if (request.FILES or None) is not None:
                    if not formset.is_valid():
                        context=addTmcAuth({
                            'form': form,
                            'formset': formset,
                        },request.user)
                        for ele in formset:
                            messages.add_message(request, messages.WARNING, str(ele))
                        return render(request, 'failuer_reports/edit.html', context)
                form.save()
                formset.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                return redirect('failuer_report_list')
            context = addTmcAuth({
                'form': form,
                'formset': formset,
                },
                 request.user)
            return render(request, 'failuer_reports/edit.html', context)
        else:
            messages.add_message(request, messages.WARNING,'他官署の情報は変更できません')
    else:
        messages.add_message(request, messages.WARNING,'該当情報はありません')
    return redirect('failuer_report_list')

@login_required
def failuer_report_detail(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    files = AttachmentFile.objects.filter(info=info)
    if info:
        context ={
            'info': info,
            'files': files,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'failuer_reports/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')

@login_required
def failuer_report_del(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    if info:
        if info.created_by==request.user:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
            return redirect('failuer_report_list')
        else:
            messages.add_message(request, messages.WARNING,'他官署の情報は削除できません')
    else:
        messages.add_message(request, messages.WARNING, '該当Infoは既に削除されてありません。')
        return redirect('failuer_report_list')
