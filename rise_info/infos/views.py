
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from .exportInfo import makeInfoSheet
from .models import Info, AttachmentFile, InfoComments, InfoTypeChoices
from .forms import InfoForm, FileFormSet, InfoCommentsForm
from accounts.views import addIsStaff, User_mail_config
from addresses.models import Addresses, RoleInLocal
from offices.models import Office
from rise_info.settings import EMAIL_HOST_USER

from datetime import datetime
from re import T
from functools import reduce
import operator
import openpyxl
import pytz


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
    model = Info
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
                    Q(select_register='under_renewal') |
                    Q(select_register='register')
            ).filter(disclosure_date__lte=datetime.today())

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
        return queryset.order_by('-disclosure_date')

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
    info = Info.objects.get_or_none(pk=info_id)
    files = AttachmentFile.objects.filter(info=info)
    if info:
        context = {
            'info': info,
            'files': files,
        }
        context = addIsStaff(context, request.user)
        return render(request, 'infos/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')


@login_required
def info_del(request, info_id):
    if request.user.is_staff:
        info = Info.objects.get_or_none(pk=info_id)
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


@login_required
def info_edit(request, info_id):
    if request.user.is_staff:
        info = Info.objects.get_or_none(pk=info_id)
        if info:
            form = InfoForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
            if (request.method == "POST" and form.is_valid()):
                if (request.FILES or None) is not None:
                    if not formset.is_valid():
                        context = addIsStaff({
                            'form': form,
                            'formset': formset,
                        }, request.user)
                        for ele in formset:
                            messages.add_message(
                                request, messages.WARNING, str(ele))
                        return render(request, 'infos/edit.html', context)
                form.save()
                formset.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                if request.POST.get("sendMailFLG"):
                    return redirect('info_send', info_id=info.pk)
                else:
                    return redirect('info_list')
            context = addIsStaff({
                'form': form,
                'formset': formset,
            },
                request.user)
            return render(request, 'infos/edit.html', context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')


@login_required
def info_new(request):
    if request.user.is_staff:
        form = InfoForm(request.POST or None)
        context = addIsStaff({'form': form}, request.user)
        if request.method == "POST" and form.is_valid():
            info = form.save(commit=False)
            formset = FileFormSet(request.POST, request.FILES, instance=info)
            if formset.is_valid():
                info.save()
                formset.save()
                form.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                if request.POST.get("sendMailFLG"):
                    return redirect('info_send', info_id=info.pk)
                else:
                    return redirect('info_list')
            else:
                context['formset'] = formset
        else:
            context['formset'] = FileFormSet()
        return render(request, "infos/new.html", context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')


@login_required
def sendmail(request, info_id):
    info = Info.objects.get_or_none(pk=info_id)
    user_mail_config = User_mail_config.objects.get_or_none(user=request.user)
    roles = RoleInLocal.objects.filter(
        info_type_relations__info_type=info.info_type)
    q_role = reduce(operator.or_, (Q(role__id__contains=i.id)for i in roles))
    is_HTML = Q(is_HTML_mail=True)
    is_Text = Q(is_HTML_mail=False)
    send_HTML_list = Addresses.object.filter(q_role).filter(is_HTML)
    send_Text_list = Addresses.object.filter(q_role).filter(is_Text)
    if info:
        context = {
            'info': info,
            'send_HTML_list': send_HTML_list,
            'send_Text_list': send_Text_list,
            'mail_config': user_mail_config,
        }
        if request.method == 'POST':
            if user_mail_config.email_address:
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
                    Addresses.object.get_or_none(pk=is_send).mail)
            for is_send in is_send_Text_list:
                dist_Text_list.append(
                    Addresses.object.get_or_none(pk=is_send).mail)
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
                return redirect('info_list')
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, '送信されませんでした。\n' + str(type(e)) + '\n' + str(e))

                return redirect('info_list')
        else:
            context = addIsStaff(context, request.user)
            return render(request, 'infos/mail_form.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')
