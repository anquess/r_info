from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import TechSupports, AttachmentFile, TechSupportComments
from .forms import TechSupportCommentsForm, TechSupportsForm, FileFormSet
from accounts.views import addIsStaff
from addresses.models import Addresses
from offices.models import Office
from rise_info.commonSend import addCommentSendMail, add_addresses,\
    notifyRegistration


class TechSupportList(ListView):
    model = TechSupports
    template_name = 'tech_supports/tech_support_list.html'
    context_object_name = 'infos'
    ordering = 'updated_at'
    paginate_by = 20

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(TechSupportList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        q_default = Q(select_register__in=['register', 'doing', 'done']) | \
            Q(created_by__username__contains=self.request.user)
        queryset = super().get_queryset(**kwargs).filter(q_default)
        key_keyword = self.request.GET.get('keyword')
        key_eqtype = self.request.GET.get('eqtype')
        key_office = self.request.GET.get('office')

        if key_eqtype is not None:
            if len(key_eqtype) > 0:
                queryset = queryset.filter(
                    Q(eqtypes__id__icontains=key_eqtype)).distinct()
        if key_office is not None and key_office != "":
            queryset = queryset.filter(
                Q(created_by__username=key_office)).distinct()
        if key_keyword is not None:
            queryset = queryset.filter(
                Q(title__contains=key_keyword) |
                Q(inquiry__contains=key_keyword) |
                Q(content__contains=key_keyword)
            ).distinct()

        return queryset.order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = addIsStaff(context, self.request.user)
        context['offices'] = Office.objects.all()
        context['selelcted_office'] = self.request.GET.get('office')
        return context


def get_form_context(request, info_id=None):
    if info_id:
        info = TechSupports.objects.get_or_none(pk=info_id)
        if info:
            form = TechSupportsForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None,
                                  files=request.FILES or None, instance=info)
        else:
            return None
    else:
        form = TechSupportsForm(request.POST or None)
        if (request.method == "POST" and form.is_valid()):
            info = form.save(commit=False)
            formset = FileFormSet(request.POST, request.FILES, instance=info)
        else:
            info = None
            formset = FileFormSet()
    addresses = Addresses.objects.filter(created_by=request.user)
    return addIsStaff({
        'form': form, 'formset': formset, 'info': info, 'info_id': info_id,
        'addresses': addresses, 'tech_supo': True, },
        request.user)


def support_update(request, info_id=None):
    context = get_form_context(request=request, info_id=info_id)
    if context:
        if (request.method == "POST" and context['form'].is_valid()):
            if context['formset'].is_valid():
                info = context['form'].save()
                context['formset'].save()
                add_addresses = request.POST.getlist('add_addresses[]')
                for address in info.addresses.all():
                    if address.created_by == request.user \
                            and not(address in add_addresses):
                        info.addresses.remove(address)
                for address in add_addresses:
                    info.addresses.add(address)
                info.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                if info.select_register == 'register':
                    notifyRegistration(info=info, request=request)
                    # if e == 1:
                    #    messages.add_message(request, messages.INFO, '通知しました。')
                    #    messages.add_message(
                    #        request, messages.INFO, '送信されませんでした。\n' + str(type(e)) + '\n' + str(e))
                    # else:
                    #    messages.add_message(
                    #        request, messages.ERROR, '送信されませんでした。\n' + str(type(e)) + '\n' + str(e))
                return redirect('support_list')
            else:
                for ele in context['formset']:
                    messages.add_message(
                        request, messages.WARNING, str(ele))
                return render(request,
                              'tech_supports/techSupportNewOrEdit.html',
                              context)
        return render(request,
                      'tech_supports/techSupportNewOrEdit.html',
                      context)
    else:
        messages.add_message(request, messages.ERROR, '当該官署発信情報はありません')
        return redirect('support_list')


@login_required
def support_edit(request, info_id):
    return support_update(request=request, info_id=info_id)


@login_required
def support_new(request):
    return support_update(request=request)


@login_required
def support_detail(request, info_id):
    info = TechSupports.objects.get_or_none(pk=info_id)
    if request.method == "POST":
        add_addresses(request=request, info=info)
        messages.add_message(request, messages.INFO, "配信先を変更しました")
        return redirect('support_list')
    files = AttachmentFile.objects.filter(info=info)
    addresses = Addresses.objects.filter(created_by=request.user)
    if info:
        context = {
            'info': info,
            'files': files,
            'addresses': addresses,
            'tech_supo': True,
        }
        context = addIsStaff(context, request.user)
        context['is_support'] = True
        return render(request, 'tech_supports/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当官署発信情報はありません。")
        return redirect('support_list')


@login_required
def support_del(request, info_id):
    if request.user.is_staff:
        info = TechSupports.objects.get_or_none(pk=info_id)
        if info:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
            return redirect('support_list')
        else:
            messages.add_message(request, messages.WARNING,
                                 '該当技術支援情報は既に削除されてありません。')
            return redirect('support_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('support_list')


@login_required
def add_comment(request, info_id):
    form = TechSupportCommentsForm(request.POST or None, request.FILES)
    if request.method == "POST" and form.is_valid():
        comment = form.save(commit=False)
        comment.save()
        messages.add_message(request, messages.INFO, '更新されました。')
        if not addCommentSendMail(comment, 'tech_support', request=request):
            messages.add_message(request, messages.ERROR, '送信されませんでした')
        return redirect('support_list')
    else:
        messages.add_message(request, messages.INFO, '値がおかしいです。')
    return redirect('/tech_support/' + str(info_id) + '/')


@login_required
def del_comment(request, info_id, comment_id):
    comment = TechSupportComments.objects.get_or_none(pk=comment_id)
    if comment:
        comment.delete()
        messages.add_message(request, messages.INFO, 'コメントは削除されました。')
        return redirect('/tech_support/' + str(info_id) + '/')
    else:
        messages.add_message(request, messages.WARNING, '該当コメントは既に削除されてありません。')
        return redirect('/tech_support/' + str(info_id) + '/')
