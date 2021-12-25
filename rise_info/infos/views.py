from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

from infos.models import Info
from infos.forms import InfoForm
from accounts.views import isInTmcGroup, addTmcAuth

@login_required
def info_list(request):
    infos = Info.objects.all()
    context = {'infos':infos}
    context = addTmcAuth(context, request.user)
    return render(request, "infos/info_list.html", context)    

@login_required
def info_new(request):
    if isInTmcGroup(request.user):
        if request.method == 'POST':
            form = InfoForm(request.POST)
            if form.is_valid():
                info = form.save(commit=False)
                info.created_by = request.user
                info.save()
                return redirect('info_list')
            else:
                raise Http404(form.errors)
        else:
            form = InfoForm()
            context = addTmcAuth({'form': form}, request.user)
        return render(request, "infos/info_new.html", context)
    else:
        raise Http404("この権限では登録は許可されていません。")

@login_required
def info_edit(request, info_id):
    info = get_object_or_404(Info, pk=info_id)
    if isInTmcGroup(request.user):
        if request.method == "POST":
            form = InfoForm(request.POST, instance=info)
            if form.is_valid():
                form.save()
                return redirect('info_list')
        else:
            form = InfoForm(instance=info)
        return render(request, 'infos/info_edit.html', {'form': form })

    else:
        raise Http404("この権限では編集は許可されていません。")

@login_required
def info_detail(request, info_id):
    info = Info.objects.get_or_none(pk=info_id)
    if info:
        context ={
            'info': info,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'infos/info_detail.html', context)
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
