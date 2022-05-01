from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from contents.models import Menu, Contents, AttachmentFile


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
