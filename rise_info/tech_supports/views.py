from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import TechSupports, AttachmentFile, TechSupportComments
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
