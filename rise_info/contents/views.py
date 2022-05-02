from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from contents.models import Menu, Contents, AttachmentFile
from contents.forms import ContentsForm, FileFormSet


def addMenus(context: dict) -> dict:
    context['menus'] = Menu.objects.order_by('sort_num').all()
    return context


@login_required
def content_detail(request, content_id):
    info = Contents.objects.get_or_none(pk=content_id)
    files = AttachmentFile.objects.filter(info=info)
    from accounts.views import addTmcAuth
    if info:
        context = {
            'info': info,
            'files': files,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'contents/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Contentsはありません。")
        return redirect('top')


@login_required
def content_edit(request, content_id):
    from accounts.views import addTmcAuth, isInTmcGroup
    if isInTmcGroup(request.user):
        info = Contents.objects.get_or_none(pk=content_id)
        if info:
            form = ContentsForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
            if (request.method == "POST" and form.is_valid()):
                if (request.FILES or None) is not None:
                    if not formset.is_valid():
                        context = addTmcAuth({
                            'form': form,
                            'formset': formset,
                        }, request.user)
                        for ele in formset:
                            messages.add_message(
                                request, messages.WARNING, str(ele))
                        return render(request, 'contents/edit.html', context)
                form.save()
                formset.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                return redirect('top')
            context = addTmcAuth({
                'form': form,
                'formset': formset,
            },
                request.user)
            return render(request, 'infos/edit.html', context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')
