from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from contents.models import ContentComments, Menu, Contents, AttachmentFile
from contents.forms import ContentsForm, FileFormSet, MenuForm, ContentCommentsForm


def content_updown(request, content_id, order):
    from accounts.views import isInTmcGroup
    if isInTmcGroup(request.user):
        menu = Contents.objects.get_or_none(pk=content_id).menu
        subject = None
        for content in Contents.objects.filter(menu=menu).order_by(order).all():
            if content.id == content_id:
                try:
                    content.replace_sort_num(subject)
                    messages.add_message(
                        request, messages.INFO, content.title + "メニューを動かしました")
                except ValueError:
                    messages.add_message(
                        request, messages.ERROR, "これより上はありません")
                return redirect('menu_list')
            else:
                subject = content
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def content_detail(request, content_id):
    info = Contents.objects.get_or_none(pk=content_id)
    files = AttachmentFile.objects.filter(info=info)
    from accounts.views import addTmcAuth
    if info:
        context = {
            'info': info,
            'files': files,
            'is_content': True,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'contents/content_detail.html', context)
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
                        return render(request, 'contents/content_edit.html', context)
                form.save()
                formset.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                return redirect('menu_list')
            context = addTmcAuth({
                'form': form,
                'formset': formset,
            },
                request.user)
            return render(request, 'contents/content_edit.html', context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def content_del(request, content_id):
    from accounts.views import isInTmcGroup
    if isInTmcGroup(request.user):
        info = Contents.objects.get_or_none(pk=content_id)
        if info:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
        else:
            messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('menu_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def content_new(request):
    from accounts.views import addTmcAuth, isInTmcGroup
    if isInTmcGroup(request.user):
        form = ContentsForm(request.POST or None)
        context = addTmcAuth({'form': form}, request.user)
        if request.method == "POST" and form.is_valid():
            info = form.save(commit=False)
            formset = FileFormSet(request.POST, request.FILES, instance=info)
            if formset.is_valid():
                info.save()
                formset.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                return redirect('menu_list')
            else:
                context['formset'] = formset
        else:
            menu_id = request.GET.get('menu')
            if Menu.objects.filter(id=menu_id).exists:
                menu = Menu.objects.get(id=menu_id)
                form = ContentsForm(request.POST or None,
                                    initial={'menu': menu, })
                context = addTmcAuth({'form': form}, request.user)

            context['menu_id'] = menu
            context['formset'] = FileFormSet()
        return render(request, "contents/content_new.html", context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def content_up(request, content_id):
    return content_updown(request, content_id, 'sort_num')


@login_required
def content_down(request, content_id):
    return content_updown(request, content_id, '-sort_num')


def addMenus(context: dict) -> dict:
    context['menus'] = Menu.objects.order_by('sort_num').prefetch_related(
        'related_content')
    return context


def menu_updown(request, menu_id, order):
    from accounts.views import isInTmcGroup
    if isInTmcGroup(request.user):
        subject = None
        for menu in Menu.objects.order_by(order).all():
            if menu.id == menu_id:
                try:
                    menu.replace_sort_num(subject)
                    messages.add_message(
                        request, messages.INFO, menu.menu_title + "メニューを動かしました")
                except ValueError:
                    messages.add_message(
                        request, messages.ERROR, "これより上はありません")
                return redirect('menu_list')
            else:
                subject = menu
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('menu_list')


@login_required
def menu_list(request):
    from accounts.views import addTmcAuth, isInTmcGroup
    if isInTmcGroup(request.user):
        context = {}
        context = addTmcAuth(context, request.user)
        return render(request, 'contents/menu_list.html', context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def menu_new(request):
    from accounts.views import isInTmcGroup
    if isInTmcGroup(request.user):
        form = MenuForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            menu = form.save(commit=False)
            menu.create()
            messages.add_message(request, messages.INFO,
                                 str(menu) + 'が登録されました。')
        return redirect('menu_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def menu_edit(request, menu_id):
    from accounts.views import isInTmcGroup
    if isInTmcGroup(request.user):
        menu = Menu.objects.get_or_none(pk=menu_id)
        if menu:
            form = MenuForm(request.POST or None, instance=menu)
            if (request.method == "POST" and form.is_valid()):
                form.save()
                messages.add_message(request, messages.INFO, '更新されました。')
        return redirect('menu_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def menu_del(request, menu_id):
    from accounts.views import isInTmcGroup
    if isInTmcGroup(request.user):
        menu = Menu.objects.get_or_none(pk=menu_id)
        if menu:
            title = menu.menu_title
            menu.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
        else:
            messages.add_message(request, messages.WARNING, "該当Menuはありません。")
        return redirect('menu_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def menu_up(request, menu_id):
    return menu_updown(request, menu_id, 'sort_num')


@login_required
def menu_down(request, menu_id):
    return menu_updown(request, menu_id, '-sort_num')


@login_required
def add_comment(request, content_id):
    form = ContentCommentsForm(request.POST or None, request.FILES)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.save()
        messages.add_message(request, messages.INFO, '更新されました。')
    else:
        messages.add_message(request, messages.INFO, '値がおかしいです。')
    return redirect('/contents/' + str(content_id) + '/')


@login_required
def del_comment(request, content_id, comment_id):
    comment = ContentComments.objects.get_or_none(pk=comment_id)
    if comment:
        comment.delete()
        messages.add_message(request, messages.INFO, 'コメントは削除されました。')
        return redirect('/contents/' + str(content_id) + '/')
    else:
        messages.add_message(request, messages.WARNING, '該当コメントは既に削除されてありません。')
        return redirect('/contents/' + str(content_id) + '/')
