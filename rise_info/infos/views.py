from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .exportInfo import makeInfoSheet
from .models import AttachmentFile, InfoComments, InfoTypeChoices, InfoRelation, Info
from .forms import InfoForm, FileFormSet, InfoCommentsForm
from accounts.views import addIsStaff, User_mail_config
from addresses.models import Addresses, RoleInLocal
from offices.models import Office
from rise_info.choices import RegisterStatusChoices
from rise_info.settings import EMAIL_HOST_USER, DEBUG
from rise_info.commonSend import addCommentSendMail, add_addresses

from functools import reduce
import operator
import openpyxl


def exportInfo(request):
    # 新規ブック作成
    wb = openpyxl.Workbook()
    ws = wb.active
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=posts.xlsx'
    makeInfoSheet(ws)
    wb.save(response)
    return response


class InfoList(ListView):
    model = InfoRelation
    template_name = 'infos/info_list.html'
    context_object_name = 'infos'
    ordering = '-updated_at'
    paginate_by = 20

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InfoList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        is_all = self.request.GET.get('is_all')
        if is_all:
            queryset = super().get_queryset(**kwargs)
        else:
            queryset = super().get_queryset(
                **kwargs).filter(
                    Q(send_info__isnull=False))

        q_info_type = self.request.GET.get('info_type')
        q_keyword = self.request.GET.get('keyword')
        q_eqtype = self.request.GET.get('eqtype')
        q_office = self.request.GET.get('office')

        if q_info_type is not None and q_info_type != "":
            queryset = queryset.filter(Q(info_type__iexact=q_info_type))
        if q_eqtype is not None:
            if len(q_eqtype) > 0:
                queryset = queryset.filter(Q(eqtypes__id__icontains=q_eqtype) | Q(
                    is_add_eqtypes__exact=False)).distinct()
        if q_office is not None and q_office != "":
            queryset = queryset.filter(Q(offices__id__icontains=q_office) | Q(
                is_add_offices__exact=False)).distinct()
        if q_keyword is not None:
            queryset = queryset.filter(
                Q(title__contains=q_keyword) |
                Q(sammary__contains=q_keyword) |
                Q(content__contains=q_keyword)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = addIsStaff(context, self.request.user)
        context['offices'] = Office.objects.all()
        context['info_types'] = InfoTypeChoices.choices
        context['selelcted_info_type'] = self.request.GET.get('info_type')
        context['selelcted_office'] = self.request.GET.get('office')
        return context


@login_required
def add_comment(request, info_id):
    form = InfoCommentsForm(request.POST or None, request.FILES)

    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.save()
        messages.add_message(request, messages.INFO, '更新されました。')
        addCommentSendMail(comment, 'infos', request)
        return redirect('info_list')

    else:
        messages.add_message(request, messages.INFO, '値がおかしいです。')
    return redirect('/infos/' + str(info_id) + '/')


@login_required
def del_comment(request, info_id, comment_id):
    comment = InfoComments.objects.get_or_none(pk=comment_id)
    if comment:
        comment.delete()
        messages.add_message(request, messages.INFO, 'コメントは削除されました。')
        return redirect('/infos/' + str(info_id) + '/')
    else:
        messages.add_message(request, messages.WARNING, '該当コメントは既に削除されてありません。')
        return redirect('/infos/' + str(info_id) + '/')


@login_required
def info_detail(request, info_id):
    info = InfoRelation.objects.get_or_none(pk=info_id)
    if info:
        if info.send_info:
            return redirect('info_detail', info.send_info.id)
    else:
        info = Info.objects.get_or_none(pk=info_id)
    files = AttachmentFile.objects.filter(info=info)
    addresses = Addresses.objects.filter(created_by=request.user)
    if request.method == "POST":
        add_addresses(request=request, info=info)
        messages.add_message(request, messages.INFO, "配信先を変更しました")
        return redirect('info_list')
    if info:
        context = {
            'info': info,
            'files': files,
            'addresses': addresses,
        }
        context = addIsStaff(context, request.user)
        return render(request, 'infos/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当TMC発信情報はありません。")
        return redirect('info_list')


@login_required
def info_del(request, info_id):
    info = Info.objects.get_or_none(pk=info_id)
    if hasattr(info, 'sended'):
        return redirect('info_del', info.sended.id)

    if request.user.is_staff:
        info = InfoRelation.objects.get_or_none(pk=info_id)
        if info:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
            return redirect('info_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 '該当Infoは既に削除されてありません。')
            return redirect('info_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')


def info_update(request, info_id=None):
    info = Info.objects.get_or_none(pk=info_id)
    if hasattr(info, 'sended'):
        return redirect('info_edit', info.sended.id)
    if request.user.is_staff:
        if info_id:
            info = InfoRelation.objects.get_or_none(pk=info_id)
            form = InfoForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
        else:
            form = InfoForm(request.POST or None)
            context = addIsStaff({'form': form}, request.user)
            if request.method == "POST" and form.is_valid():
                info = form.save(commit=False)
                formset = FileFormSet(
                    request.POST, request.FILES, instance=info)
            else:
                info = None
                formset = FileFormSet()
        addresses = Addresses.objects.filter(
            created_by=request.user)
        context = addIsStaff({
            'form': form, 'formset': formset,
            'info': info, 'info_id': info_id,
            'addresses': addresses, },
            request.user)
        if request.method == "POST" and form.is_valid():
            if (request.FILES or None) is not None:
                if not formset.is_valid():
                    for ele in formset:
                        messages.add_message(
                            request, messages.WARNING, str(ele))
                    return render(request, 'infos/infoNewOrEdit.html', context)
            form.save()
            formset.save()
            add_addresses = request.POST.getlist('add_addresses[]')
            for address in info.addresses.all():
                if address.created_by == request.user \
                        and not(address in add_addresses):
                    info.addresses.remove(address)
            for address in add_addresses:
                info.addresses.add(address)
            info.save()
            if info_id:
                messages.add_message(request, messages.INFO, '更新されました。')
            else:
                messages.add_message(request, messages.INFO, '登録されました。')
            if request.POST.get("sendMailFLG"):
                return redirect('info_send', info_id=info.pk)
            else:
                return redirect('info_list')
        else:
            return render(request, 'infos/infoNewOrEdit.html', context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')


@login_required
def info_new(request):
    return info_update(request=request)


@login_required
def info_edit(request, info_id):
    return info_update(request=request, info_id=info_id)


@login_required
def sendmail(request, info_id):
    info = Info.objects.get_or_none(pk=info_id)
    if hasattr(info, 'sended'):
        return redirect('info_send', info.sended.id)
    info = InfoRelation.objects.get_or_none(pk=info_id)
    user_mail_config = User_mail_config.objects.get_or_none(user=request.user)
    roles = RoleInLocal.objects.filter(
        info_type_relations__info_type=info.info_type)
    q_role = reduce(operator.or_, (Q(role__id__contains=i.id)for i in roles))
    is_HTML = Q(is_HTML_mail=True)
    is_Text = Q(is_HTML_mail=False)
    send_HTML_list = Addresses.objects.filter(q_role).filter(is_HTML)
    send_Text_list = Addresses.objects.filter(q_role).filter(is_Text)
    if info:
        context = {
            'info': info,
            'send_HTML_list': send_HTML_list,
            'send_Text_list': send_Text_list,
            'mail_config': user_mail_config,
        }
        if request.method == 'POST':
            if user_mail_config.email_address and not DEBUG:
                sendmail_adr = user_mail_config.email_address
            else:
                sendmail_adr = EMAIL_HOST_USER
            subject = request.POST.get("subject")
            context['mail_header'] = request.POST.get("header")
            context['mail_footer'] = request.POST.get("footer")
            dist_HTML_list = []
            dist_Text_list = []
            is_send_HTML_list = request.POST.getlist('is_send_HTML_list[]')
            is_send_Text_list = request.POST.getlist('is_send_Text_list[]')
            msg_plain = render_to_string('infos/mail.txt', context)
            msg_HTML = render_to_string('infos/mail.html', context)
            for is_send in is_send_HTML_list:
                dist_HTML_list.append(
                    Addresses.objects.get_or_none(pk=is_send).mail)
            for is_send in is_send_Text_list:
                dist_Text_list.append(
                    Addresses.objects.get_or_none(pk=is_send).mail)
            try:
                send_mail(
                    subject,
                    msg_plain,
                    sendmail_adr,
                    dist_HTML_list,
                    html_message=msg_HTML,
                    fail_silently=False,
                )
                send_mail(
                    subject,
                    msg_plain,
                    sendmail_adr,
                    dist_Text_list,
                    fail_silently=False,
                )
                messages.add_message(request, messages.INFO, '送信されました。')
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, '送信されませんでした。\n' + str(type(e)) + '\n' + str(e))
            if info.send_info:
                info.send_info.title = info.title
                info.send_info.content = info.content
                info.send_info.created_by = info.created_by
                info.send_info.created_at = info.created_at
                info.send_info.updated_at = info.updated_at
                info.send_info.updated_by = info.updated_by
                info.send_info.info_type = info.info_type
                info.send_info.is_rich_text = info.is_rich_text
                info.send_info.managerID = info.managerID
                info.send_info.sammary = info.sammary
                info.send_info.is_add_eqtypes = info.is_add_eqtypes
                info.send_info.is_add_offices = info.is_add_offices
                if info.offices.all():
                    info.send_info.offices = info.offices
                if info.eqtypes.all():
                    info.send_info.eqtypes = info.eqtypes
                if info.addresses.all():
                    info.send_info.addresses = info.addresses
                info.send_info.select_register = RegisterStatusChoices.REGISTER
                info.send_info.save()
            else:
                send_info = info.info_ptr
                send_info.id = None
                send_info.pk = None
                send_info.created_by = info.created_by
                send_info.created_at = info.created_at
                send_info.updated_by = info.updated_by
                send_info.updated_at = info.updated_at
                send_info.select_register = RegisterStatusChoices.REGISTER
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

            return redirect('info_list')
        else:
            context = addIsStaff(context, request.user)
            return render(request, 'infos/mail_form.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')
