from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.db.models import Q

from .models import Addresses
from .forms import AddressesForm
from accounts.views import addTmcAuth
from offices.models import getOffices


class AddressList(ListView):
    model = Addresses
    template_name = 'addresses/address_list.html'
    context_object_name = 'addresses'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs).filter(
            Q(created_by__username__contains=self.request.user))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = addTmcAuth(context, self.request.user)
        context['selelcted_user'] = self.request.GET.get('created_by')
        return context


@ login_required
def addresses_new(request):
    form = AddressesForm(request.POST or None)
    context = addTmcAuth({'form': form, 'is_new': True}, request.user)
    if request.method == "POST" and form.is_valid():
        new_address = form.save(commit=False)
        new_address.save()
        form.save()

        messages.add_message(request, messages.INFO, '追加されました')
        return redirect('address_list')
    return render(request, "addresses/address_edit_new.html", context)


@ login_required
def addresses_edit(request, address_id):
    address = Addresses.object.get_or_none(pk=address_id)
    if address:
        if address.created_by == request.user:
            form = AddressesForm(request.POST or None, instance=address)
            if(request.method == 'POST' and form.is_valid()):
                form.save()
                messages.add_message(request, messages.INFO, '更新されました。')
                return redirect('address_list')
            else:
                context = addTmcAuth({'form': form, }, request.user)
                return render(request, "addresses/address_edit_new.html", context)
        else:
            messages.add_message(request, messages.WARNING,
                                 '他官署が管理する配信先は編集できません')
    else:
        messages.add_message(request, messages.WARNING, '該当配信先は既に削除されてありません。')
    return redirect('address_list')


@ login_required
def addresses_del(request, address_id):
    address = Addresses.object.get_or_none(pk=address_id)
    if address:
        if address.created_by == request.user:
            positon = address.position
            name = address.name
            address.delete()
            messages.add_message(request, messages.INFO,
                                 '役職:%s 氏名:%s は削除されました。' % (positon, name))
        else:
            messages.add_message(request, messages.WARNING,
                                 '他官署が管理する配信先は削除できません')
    else:
        messages.add_message(request, messages.WARNING, '該当配信先は既に削除されてありません。')
    return redirect('address_list')
