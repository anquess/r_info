from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import TechSupports, AttachmentFile, TechSupportComments
from .forms import TechSupportCommentsForm, TechSupportsForm, FileFormSet
from accounts.views import isInTmcGroup, addTmcAuth
from offices.models import Office


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
        queryset = super().get_queryset(**kwargs)
        q_keyword = self.request.GET.get('keyword')
        q_eqtype = self.request.GET.get('eqtype')
        q_office = self.request.GET.get('office')

        if q_eqtype is not None:
            if len(q_eqtype) > 0:
                queryset = queryset.filter(
                    Q(eqtypes__id__icontains=q_eqtype)).distinct()
        if q_office is not None and q_office != "":
            queryset = queryset.filter(
                Q(created_by__username=q_office)).distinct()
        if q_keyword is not None:
            queryset = queryset.filter(
                Q(title__contains=q_keyword) |
                Q(inquiry__contains=q_keyword) |
                Q(content__contains=q_keyword)
            ).distinct()

        return queryset.order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = addTmcAuth(context, self.request.user)
        context['offices'] = Office.objects.all()
        context['selelcted_office'] = self.request.GET.get('office')
        return context


@login_required
def support_edit(request, info_id):
    info = TechSupports.objects.get_or_none(pk=info_id)
    if info:
        form = TechSupportsForm(request.POST or None, instance=info)
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
                    return render(request, 'tech_supports/edit.html', context)
            form.save()
            formset.save()
            messages.add_message(request, messages.INFO, '更新されました。')
            return redirect('support_list')
        context = addTmcAuth({
            'form': form,
            'formset': formset,
        },
            request.user)
        return render(request, 'tech_supports/edit.html', context)


@login_required
def support_new(request):
    form = TechSupportsForm(request.POST or None)
    context = addTmcAuth({'form': form}, request.user)
    if request.method == "POST" and form.is_valid():
        info = form.save(commit=False)
        formset = FileFormSet(request.POST, request.FILES, instance=info)
        if formset.is_valid():
            info.save()
            formset.save()
            messages.add_message(request, messages.INFO, '更新されました。')
            return redirect('support_list')
        else:
            context['formset'] = formset
    else:
        context['formset'] = FileFormSet()
    return render(request, "tech_supports/new.html", context)


@login_required
def support_detail(request, info_id):
    info = TechSupports.objects.get_or_none(pk=info_id)
    files = AttachmentFile.objects.filter(info=info)
    if info:
        context = {
            'info': info,
            'files': files,
        }
        context = addTmcAuth(context, request.user)
        context['is_support'] = True
        return render(request, 'tech_supports/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当業務支援情報はありません。")
        return redirect('support_list')


@login_required
def support_del(request, info_id):
    if isInTmcGroup(request.user):
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
