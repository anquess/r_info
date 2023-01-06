from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import ListView

from .models import FailuerReportRelation, AttachmentFile, \
    Circumstances
from .forms import FailuerReportRelationForm, FileFormSet, CircumstancesFormSet
from accounts.models import User_mail_config
from accounts.views import addIsStaff
from addresses.models import Addresses
from rise_info.choices import RegisterStatusChoicesFailuer
from rise_info.settings import EMAIL_HOST_USER, DEBUG

from functools import reduce
import operator


def get_addresses(fail_rep, is_HMTL: bool, grps):
    user_grops = grps.all()
    q_user_group = reduce(operator.or_, (
        Q(groups__id__contains=i.id)for i in user_grops
    ))
    department = fail_rep.department.all()
    q_department = reduce(operator.or_, (
        Q(department__id__contains=i.id)for i in department
    ))
    q_is_HTML = Q(is_HTML_mail=is_HMTL)

    return Addresses.objects.filter(
        q_department).filter(
        q_user_group).filter(
        q_is_HTML).distinct()


@ login_required
def sendmail(request, info_id):
    info = FailuerReportRelation.objects.get_or_none(pk=info_id)
    user_mail_config = User_mail_config.objects.get_or_none(user=request.user)
    events = Circumstances.objects.filter(info=info).order_by('-date', '-time')

    send_HTML_required = get_addresses(info, True, request.user.groups)
    send_Text_required = get_addresses(info, False, request.user.groups)
    send_HTML_any = Addresses.objects.filter(
        created_by=request.user).filter(Q(is_HTML_mail=True))
    send_Text_any = Addresses.objects.filter(
        created_by=request.user).filter(Q(is_HTML_mail=False))

    if info:
        context = {
            'info': info,
            'events': events,
            'send_HTML_required_list': send_HTML_required,
            'send_Text_required_list': send_Text_required,
            'send_HTML_any_list': send_HTML_any,
            'send_Text_any_list': send_Text_any,
            'mail_config': user_mail_config,
        }
        if request.method == "POST":
            if user_mail_config.email_address and not DEBUG:
                email1 = user_mail_config.email_address
            else:
                email1 = EMAIL_HOST_USER

            if request.POST.get("subject"):
                subject = request.POST.get("subject")
            else:
                subject = "【障害通報】" + str(info.title)
            if request.POST.get("header"):
                context['mail_header'] = request.POST.get("header")
            else:
                context['mail_header'] = None
            if request.POST.get("footer"):
                context['mail_footer'] = request.POST.get("footer")
            else:
                context['mail_footer'] = None

            is_send_list = request.POST.getlist('is_send_list[]')
            dist_HTML_list = []
            dist_Text_list = []
            dist_list = []
            msg_plain = render_to_string('failuer_reports/mail.txt', context)
            msg_html = render_to_string('failuer_reports/mail.html', context)
            for is_send in is_send_list:
                adr = Addresses.objects.get_or_none(pk=is_send)
                dist_list.append(adr)
                if adr.is_HTML_mail:
                    dist_HTML_list.append(adr.mail)
                else:
                    dist_HTML_list.append(adr.mail)
            try:
                send_mail(
                    subject=subject,
                    message=msg_plain,
                    from_email=email1,
                    recipient_list=dist_HTML_list,
                    html_message=msg_html,
                    fail_silently=False,
                )
                send_mail(
                    subject=subject,
                    message=msg_plain,
                    from_email=email1,
                    recipient_list=dist_Text_list,
                    fail_silently=False,
                )
            except Exception as e:
                messages.add_message(
                    request, messages.ERROR, '送信されませんでした。\n' + str(type(e)) +
                    '\n' + str(e) + '\n' + str(is_send_list))
            if info.recovery_time:
                select_register = RegisterStatusChoicesFailuer.SENDED
            else:
                select_register = RegisterStatusChoicesFailuer.DONE
            if info.send_repo:
                info.send_repo.title = info.title
                info.send_repo.content = info.content
                info.send_repo.created_by = info.created_by
                info.send_repo.created_at = info.created_at
                info.send_repo.updated_at = info.updated_at
                info.send_repo.updated_by = info.updated_by
                info.send_repo.failuer_date = info.failuer_date
                info.send_repo.failuer_time = info.failuer_time
                info.send_repo.date_time_confirmation = \
                    info.date_time_confirmation
                info.send_repo.failuer_place = info.failuer_place
                info.send_repo.eq = info.eq
                info.send_repo.notam = info.notam
                info.send_repo.cause = info.cause
                info.send_repo.sammary = info.sammary
                info.send_repo.recovery_date = info.recovery_date
                info.send_repo.recovery_time = info.recovery_time
                info.send_repo.recovery_propects = info.recovery_propects
                info.send_repo.is_flight_impact = info.is_flight_impact
                info.send_repo.flight_impact = info.flight_impact
                info.send_repo.is_press = info.is_press
                info.send_repo.press_contents = info.press_contents
                info.send_repo.select_register = select_register
                info.send_repo.save()
            else:
                send_repo = info.failuerreport_ptr
                send_repo.id = None
                send_repo.pk = None
                send_repo.select_register = select_register
                send_repo.save()
                info.send_repo = send_repo
            info.dest_list.all().delete()
            for adr in dist_list:
                info.dest_list.add(adr)
            info.mail_title = subject
            info.mail_header = context['mail_header']
            info.mail_footer = context['mail_footer']
            info.save()
            messages.add_message(request, messages.INFO, '送信されました。')
            return redirect('failuer_report_list')

        else:
            context = addIsStaff(context, request.user)
            return render(request, 'failuer_reports/mail_form.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当障害通報書はありません。")
        return redirect('failuer_report_list')


class FailuerReportRelationList(ListView):
    model = FailuerReportRelation
    template_name = 'failuer_reports/list.html'
    context_object_name = 'infos'
    ordering = '-updated_at'
    paginate_by = 20

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FailuerReportRelationList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        is_all = self.request.GET.get('is_all')
        if is_all:
            queryset = super().get_queryset(**kwargs).filter(
                Q(created_by__username__contains=self.request.user))
        else:
            queryset = super().get_queryset(**kwargs).filter(
                Q(created_by__username__contains=self.request.user) |
                Q(send_repo__isnull=False))
        q_created_by = self.request.GET.get('created_by')
        q_keyword = self.request.GET.get('keyword')
        if q_created_by is not None:
            queryset = queryset.filter(
                Q(created_by__username__contains=q_created_by)
            ).distinct()
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
        context['users'] = User.objects.all()
        context['selelcted_user'] = self.request.GET.get('created_by')
        return context


@ login_required
def failuer_report_new(request):
    form = FailuerReportRelationForm(request.POST or None)
    context = addIsStaff({'form': form}, request.user)
    if request.method == "POST" and form.is_valid():
        info = form.save(commit=False)
        formset = FileFormSet(request.POST, request.FILES,
                              instance=info or None)
        formset2 = CircumstancesFormSet(request.POST, instance=info or None)
        if not formset.is_valid():
            for k in formset.errors:
                print(k, formset.errors[k][0])
            print(formset.non_form_errors())
        if not formset2.is_valid():
            for k in formset2.errors:
                print(k, formset2.errors[k][0])
            print(formset2.non_form_errors())

        if formset.is_valid() and formset2.is_valid():
            info.created_by = request.user
            info.save()
            formset.save()
            formset2.save()
            form.save()
            messages.add_message(request, messages.INFO, '更新されました。')
            if request.POST.get("sendMailFLG"):
                return redirect('send_mail', info_id=info.pk)
            else:
                return redirect('failuer_report_list')
        else:
            context['formset'] = formset
            context['formset2'] = formset2
    else:
        context['formset'] = FileFormSet()
        context['formset2'] = CircumstancesFormSet()
    return render(
        request,
        "failuer_reports/failuerReportsNewOrEdit.html",
        context)


@ login_required
def failuer_report_edit(request, info_id):
    info = FailuerReportRelation.objects.get_or_none(pk=info_id)
    if info:
        if info.created_by == request.user:
            form = FailuerReportRelationForm(
                request.POST or None, files=request.FILES or None,
                instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
            formset2 = CircumstancesFormSet(
                request.POST or None, instance=info)
            if (request.method == "POST" and form.is_valid()):
                if (request.FILES or None) is not None:
                    if not (formset.is_valid()):
                        context = addIsStaff({
                            'form': form,
                            'formset': formset,
                            'formset2': formset2,
                        }, request.user)
                        for ele in formset:
                            messages.add_message(
                                request, messages.WARNING, str(ele))
                        for ele in formset2:
                            messages.add_message(
                                request, messages.WARNING, str(ele))
                        return render(
                            request,
                            'failuer_reports/failuerReportsNewOrEdit.html',
                            context)
                if formset2.is_valid():
                    info = form.save(commit=False)
                    formset.save()
                    formset2.save()
                    form.save()
                    messages.add_message(request, messages.INFO, '更新されました。')
                    if request.POST.get("sendMailFLG"):
                        return redirect('send_mail', info_id=info_id)
                    else:
                        return redirect('failuer_report_list')
            context = addIsStaff({
                'form': form,
                'formset': formset,
                'formset2': formset2,
            },
                request.user)
            return render(
                request,
                'failuer_reports/failuerReportsNewOrEdit.html',
                context)
        else:
            messages.add_message(request, messages.WARNING, '他官署の情報は変更できません')
    else:
        messages.add_message(request, messages.WARNING, '該当情報はありません')
    return redirect('failuer_report_list')


@ login_required
def failuer_report_detail(request, info_id):
    relation_info = FailuerReportRelation.objects.get_or_none(pk=info_id)
    dest_list = relation_info.dest_list.all()
    if request.user == relation_info.created_by:
        info = relation_info
    else:
        info = relation_info.send_repo
    files = AttachmentFile.objects.filter(info=relation_info)
    events = Circumstances.objects.filter(
        info=relation_info).order_by('-date', '-time')
    if info:
        context = {
            'info': info,
            'files': files,
            'events': events,
            'relation_info': relation_info,
            'dest_list': dest_list,
        }
        context = addIsStaff(context, request.user)
        return render(request, 'failuer_reports/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')


@ login_required
def failuer_report_del(request, info_id):
    info = FailuerReportRelation.objects.get_or_none(pk=info_id)
    if info:
        if info.created_by == request.user:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
            return redirect('failuer_report_list')
        else:
            messages.add_message(request, messages.WARNING, '他官署の情報は削除できません')
    else:
        messages.add_message(request, messages.WARNING, '該当Infoは既に削除されてありません。')
        return redirect('failuer_report_list')
