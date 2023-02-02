from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Menu, ContentsRelation, AttachmentFile, ContentComments, Contents
from .forms import ContentsForm, FileFormSet, MenuForm, ContentCommentsForm
from accounts.views import addIsStaff
from rise_info.choices import RegisterStatusChoices


def content_updown(request, content_id, order):
    if request.user.is_staff:
        menu = ContentsRelation.objects.get_or_none(pk=content_id).menu
        subject = None
        for content in ContentsRelation.objects.filter(menu=menu).order_by(order).all():
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
    relation_info = ContentsRelation.objects.get_or_none(pk=content_id)
    if relation_info:
        if relation_info.send_info:
            return redirect('content_detail', relation_info.send_info.id)
    else:
        relation_info = Contents.objects.get_or_none(pk=content_id)

    files = AttachmentFile.objects.filter(info=relation_info)

    info = relation_info

    if info:
        context = {
            'info': info,
            'files': files,
            'is_content': True,
        }
        context = addIsStaff(context, request.user)
        return render(request, 'contents/content_detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当周知掲示板はありません。")
        return redirect('top')


@login_required
def content_del(request, content_id):
    info = Contents.objects.get_or_none(pk=info_id)
    if hasattr(info, 'sended'):
        return redirect('content_del', info.sended.id)

    if request.user.is_staff:
        info = ContentsRelation.objects.get_or_none(pk=content_id)
        if info:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
        else:
            messages.add_message(request, messages.WARNING, "該当周知掲示板はありません。")
        return redirect('menu_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


def get_form_context(request, content_id=None):
    if content_id:
        info = ContentsRelation.objects.get_or_none(pk=content_id)
        if info:
            form = ContentsForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
        else:
            return None
    else:
        form = ContentsForm(request.POST or None)
        if (request.method == "POST" and form.is_valid()):
            info = form.save(commit=False)
            formset = FileFormSet(request.POST, request.FILES, instance=info)
        else:
            info = None
            formset = FileFormSet()
    return addIsStaff({
        'form': form, 'formset': formset, 'info': info, 'info_id': content_id, },
        request.user)


def content_update(request, content_id=None):
    info = Contents.objects.get_or_none(pk=content_id)
    if hasattr(info, 'sended'):
        return redirect('content_edit', info.sended.id)

    if request.user.is_staff:
        context = get_form_context(request=request, content_id=content_id)
        if context:
            if (request.method == "POST" and context['form'].is_valid()):
                if context['formset'].is_valid():
                    info = context['form'].save()
                    context['formset'].save()
                    info.save()
                if request.POST.get("registration"):
                    if info.send_info:
                        info.send_info.title = info.title
                        info.send_info.content = info.content
                        info.send_info.created_by = info.created_by
                        info.send_info.created_at = info.created_at
                        info.send_info.updated_at = info.updated_at
                        info.send_info.updated_by = info.updated_by
                        info.send_info.menu = info.menu
                        info.send_info.select_register = \
                            RegisterStatusChoices.REGISTER
                        info.send_info.save()
                    else:
                        send_info = info.contents_ptr
                        send_info.id = None
                        send_info.pk = None
                        send_info.select_register = \
                            RegisterStatusChoices.REGISTER
                        send_info.save()
                        info.send_info = send_info
                    info.save()
                    attachments = AttachmentFile.objects.filter(info__id = info.send_info.pk)
                    for attachment in attachments:
                        attachment.delete()
                    attachments = AttachmentFile.objects.filter(info__id = info.pk)
                    for attachment in attachments:
                        attachment.id = None
                        attachment.info = info.send_info
                        attachment.save()
                    messages.add_message(request, messages.INFO, '登録されました。')
                else:
                    messages.add_message(request, messages.INFO, '一時保存されました。')
                return redirect('menu_list')
            return render(request, 'contents/contentNewOrEdit.html', context)
        else:
            messages.add_message(request, messages.WARNING, "該当周知掲示板はありません。")
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
    return redirect('top')


@login_required
def content_edit(request, content_id):
    return content_update(request=request, content_id=content_id)


@login_required
def content_new(request):
    return content_update(request=request)


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
    if request.user.is_staff:
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
    if request.user.is_staff:
        context = {}
        context = addIsStaff(context, request.user)
        return render(request, 'contents/menu_list.html', context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('top')


@login_required
def menu_new(request):
    if request.user.is_staff:
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
    if request.user.is_staff:
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
    if request.user.is_staff:
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
       for k, v in form.errors.items():
          messages.add_message(request, messages.ERROR, str(k) + str(v[0]))     
       messages.add_message(request, messages.ERROR, '値がおかしいです。')
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
