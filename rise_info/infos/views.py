from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from infos.models import Info, InfoFile
from infos.forms import InfoForm, FileFormSet
from accounts.views import isInTmcGroup, addTmcAuth

@login_required
def info_list(request):
    infos = Info.objects.all()
    context = {'infos':infos}
    context = addTmcAuth(context, request.user)
    return render(request, "infos/list.html", context)    

@login_required
def info_detail(request, info_id):
    info = Info.objects.get_or_none(pk=info_id)
    files = InfoFile.objects.filter(info=info)
    if info:
        context ={
            'info': info,
            'files': files,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'infos/detail.html', context)
    else:
        raise Http404('該当Infoはありません。')

@login_required
def info_del(request, info_id):
    if isInTmcGroup(request.user):
        info = Info.objects.get_or_none(pk=info_id)
        if info:
            title = info.title
            info.delete()
            return redirect('info_list')
        else:
            raise Http404('該当Infoは既に削除されてありません。')
    else:
        raise Http404("この権限では編集は許可されていません。")

@login_required
def info_edit(request, info_id):
    if isInTmcGroup(request.user):
        info = Info.objects.get_or_none(pk=info_id)
        if info:
            form = InfoForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None, files=request.FILES or None, instance=info)
            if (request.method == "POST" and form.is_valid()) :
                    if (request.FILES or None) is not None:
                        if not formset.is_valid():
                            return Http404(request.FILES)
                        form.save()
                        formset.save()
                        return redirect('info_list')
                        

            context = addTmcAuth({
                'form': form,
                'formset': formset,
                },
                 request.user)
            return render(request, 'infos/edit.html', context)
    else:
        raise Http404("この権限では編集は許可されていません。")
    

@login_required
def info_new(request):
    if isInTmcGroup(request.user):
        form = InfoForm(request.POST or None)
        context = addTmcAuth({'form': form}, request.user)
        if request.method == "POST" and form.is_valid():
            info = form.save(commit=False)
            formset = FileFormSet(request.POST, request.FILES, instance=info)
            if formset.is_valid():
                info.save()
                formset.save()
                return redirect('info_list')
            else:
                context['formset'] = formset
        else:
            context['formset'] = FileFormSet()
            context['model_name'] = 'infofile'
        return render(request, "infos/new.html", context)
    else:
        raise Http404("この権限では編集は許可されていません。")
