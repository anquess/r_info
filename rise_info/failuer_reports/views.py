from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


from .models import FailuerReport, AttachmentFile, Circumstances
from .forms import FailuerReportForm, FileFormSet, CircumstancesFormSet
from accounts.views import addTmcAuth
from rise_info.settings import EMAIL_HOST_USER
from rise_info.settings import EMAIL_TEST_USER


@login_required
def sendmail(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    events = Circumstances.objects.filter(info=info).order_by('-date', '-time')
    if info:
        context = {
            'info': info,
            # 'files': files,
            'events': events,
        }
        if request.method == "POST":
            email1 = EMAIL_HOST_USER

            if request.POST.get("to"):
                email2 = request.POST.get("to")
            else:
                email2 = None

            if request.POST.get("subject"):
                subject = request.POST.get("subject")
            else:
                subject = "【障害通報】" + str(info.title)
            if request.POST.get("header"):
                context['mail_header'] = request.POST.get("header")
            msg_plain = render_to_string('failuer_reports/mail.txt', context)
            msg_html = render_to_string('failuer_reports/mail.html', context)
            try:
                send_mail(
                    subject,  # Subject of the email
                    msg_plain,  # Body or Message of the email
                    # from@gmail.com   (admin@gmail.com for gmail account)
                    email1,
                    [email2],  # to@gmail.com  # email that is filled in the form
                    html_message=msg_html,
                    fail_silently=False,
                )
                messages.add_message(request, messages.INFO, '送信されました。')
                return redirect('failuer_report_list')
            except Exception:
                messages.add_message(request, messages.ERROR, '送信されませんでした。')
                return redirect('failuer_report_list')
        else:
            context = addTmcAuth(context, request.user)
            return render(request, 'failuer_reports/mail_form.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')


class FailuerReportList(ListView):
    model = FailuerReport
    template_name = 'failuer_reports/list.html'
    context_object_name = 'infos'
    ordering = '-updated_at'
    paginate_by = 20

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(FailuerReportList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        is_all = self.request.GET.get('is_all')
        if is_all:
            queryset = super().get_queryset(**kwargs).filter(
                Q(created_by__username__contains=self.request.user))
        else:
            queryset = super().get_queryset(**kwargs)
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
        context = addTmcAuth(context, self.request.user)
        context['users'] = User.objects.all()
        context['selelcted_user'] = self.request.GET.get('created_by')
        return context


@ login_required
def failuer_report_new(request):
    form = FailuerReportForm(request.POST or None)
    context = addTmcAuth({'form': form}, request.user)
    if request.method == "POST" and form.is_valid():
        info = form.save(commit=False)
        formset = FileFormSet(request.POST, request.FILES, instance=info)
        formset2 = CircumstancesFormSet(request.POST, instance=info)
        if formset.is_valid() and formset2.is_valid():
            info.created_by = request.user
            info.save()
            formset.save()
            formset2.save()
            messages.add_message(request, messages.INFO, '更新されました。')
            return redirect('failuer_report_list')
        else:
            context['formset'] = formset
            context['formset2'] = formset2
    else:
        context['formset'] = FileFormSet()
        context['formset2'] = CircumstancesFormSet()
    return render(request, "failuer_reports/new.html", context)


@ login_required
def failuer_report_edit(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    if info:
        if info.created_by == request.user:
            form = FailuerReportForm(
                request.POST or None, files=request.FILES or None, instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
            formset2 = CircumstancesFormSet(
                request.POST or None, instance=info)
            if (request.method == "POST" and form.is_valid()):
                if (request.FILES or None) is not None:
                    if not (formset.is_valid()):
                        context = addTmcAuth({
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
                        return render(request, 'failuer_reports/edit.html', context)
                if formset2.is_valid():
                    form.save()
                    formset.save()
                    formset2.save()
                    messages.add_message(request, messages.INFO, '更新されました。')
                    return redirect('failuer_report_list')
            context = addTmcAuth({
                'form': form,
                'formset': formset,
                'formset2': formset2,
            },
                request.user)
            return render(request, 'failuer_reports/edit.html', context)
        else:
            messages.add_message(request, messages.WARNING, '他官署の情報は変更できません')
    else:
        messages.add_message(request, messages.WARNING, '該当情報はありません')
    return redirect('failuer_report_list')


@ login_required
def failuer_report_detail(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
    files = AttachmentFile.objects.filter(info=info)
    events = Circumstances.objects.filter(info=info).order_by('-date', '-time')
    if info:
        context = {
            'info': info,
            'files': files,
            'events': events,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'failuer_reports/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')


@ login_required
def failuer_report_del(request, info_id):
    info = FailuerReport.objects.get_or_none(pk=info_id)
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
