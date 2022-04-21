from ast import keyword
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

from infos.models import Info, AttachmentFile
from infos.forms import InfoForm, FileFormSet
from accounts.views import isInTmcGroup, addTmcAuth

class InfoList(ListView):
    model = Info
    template_name = 'infos/info_list.html'
    context_object_name = 'infos'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InfoList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs)
        q_keyword = self.request.GET.get('keyword')
        if q_keyword is not None:
            queryset = queryset.filter(
                Q(title__contains=q_keyword)|
                Q(sammary__contains=q_keyword)|
                Q(content__contains=q_keyword)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = addTmcAuth(context, self.request.user)
        return context

@login_required
def info_detail(request, info_id):
    info = Info.objects.get_or_none(pk=info_id)
    files = AttachmentFile.objects.filter(info=info)
    if info:
        context ={
            'info': info,
            'files': files,
        }
        context = addTmcAuth(context, request.user)
        return render(request, 'infos/detail.html', context)
    else:
        messages.add_message(request, messages.WARNING, "該当Infoはありません。")
        return redirect('info_list')

@login_required
def info_del(request, info_id):
    if isInTmcGroup(request.user):
        info = Info.objects.get_or_none(pk=info_id)
        if info:
            title = info.title
            info.delete()
            messages.add_message(request, messages.INFO, '%sは削除されました。' % title)
            return redirect('info_list')
        else:
            messages.add_message(request, messages.WARNING, '該当Infoは既に削除されてありません。')
            return redirect('info_list')
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')

@login_required
def info_edit(request, info_id):
    if isInTmcGroup(request.user):
        info = Info.objects.get_or_none(pk=info_id)
        if info:
            form = InfoForm(request.POST or None, instance=info)
            formset = FileFormSet(request.POST or None, files=request.FILES or None, instance=info)
            if (request.method == "POST" and form.is_valid()) :
                    if (request.FILES or None) is not None:
                        if not formset.is_valid():
                            context=addTmcAuth({
                                'form': form,
                                'formset': formset,
                            },request.user)
                            for ele in formset:
                                messages.add_message(request, messages.WARNING, str(ele))
                            return render(request, 'infos/edit.html', context)
                    form.save()
                    formset.save()
                    messages.add_message(request, messages.INFO, '更新されました。')
                    return redirect('info_list')
            context = addTmcAuth({
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
    if isInTmcGroup(request.user):
        form = InfoForm(request.POST or None)
        context = addTmcAuth({'form': form}, request.user)
        if request.method == "POST" and form.is_valid():
            info = form.save(commit=False)
            formset = FileFormSet(request.POST, request.FILES, instance=info)
            if formset.is_valid():
                info.save()
                formset.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                return redirect('info_list')
            else:
                context['formset'] = formset
        else:
            context['formset'] = FileFormSet()
        return render(request, "infos/new.html", context)
    else:
        messages.add_message(request, messages.WARNING, "この権限では編集は許可されていません。")
        return redirect('info_list')
