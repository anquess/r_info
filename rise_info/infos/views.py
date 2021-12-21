from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from infos.models import Info
from infos.forms import InfoForm
from accounts.views import isInTmcGroup

@login_required
def info_list(request):
    infos = Info.objects.all()
    if hasattr(request, "user"):
        auth = isInTmcGroup(request.user)
    else:
        auth = None
    context = {
        "infos": infos,
        "auth": auth
        }
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
                return redirect(info_detail, info_id=info.pk)
        else:
            form = InfoForm()
        return render(request, "infos/info_new.html", {'form': form})
    else:
        return HttpResponseForbidden("この権限では登録は許可されていません。")

@login_required
def info_edit(request, info_id):
    info = get_object_or_404(Info, pk=info_id)
    if isInTmcGroup(request.user):
        if request.method == "POST":
            form = InfoForm(request.POST, instance=info)
            if form.is_valid():
                form.save()
                return redirect('info_detail', info_id=info_id)
        else:
            form = InfoForm(instance=info)
        return render(request, 'infos/info_edit.html', {'form': form })

    else:
        return HttpResponseForbidden("この権限では編集は許可されていません。")

def info_detail(request, info_id):
    if hasattr(request, "user"):
        auth = isInTmcGroup(request.user)
    else:
        auth = None
    info = get_object_or_404(Info, pk=info_id)
    return render(request, 'infos/info_detail.html', {'info': info, 'auth':auth})
