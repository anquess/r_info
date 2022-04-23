from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

import sys

from .forms import UploadFileForm
from .models import Office, offices_csv_import
from accounts.views import isInTmcGroup, addTmcAuth
from histories.models import getLastUpdateAt


@login_required
def office_del(request, office_id):
    if isInTmcGroup(request.user):
        office = Office.objects.get_or_none(pk=office_id)
        if office:
            office.unyo_sts = not office.unyo_sts
            office.save()
            unyo_str = '有効' if office.unyo_sts else '無効'
            messages.add_message(request, messages.INFO,
                                 f'{office.name}の運用状態は{unyo_str}になりました。')
        else:
            messages.add_message(request, messages.WARNING, '削除対象は既に削除されています')
    else:
        messages.add_message(request, messages.WARNING, 'この権限では許可されていません。')
    return redirect('office')


@login_required
def file_upload(request):
    if isInTmcGroup(request.user):
        if request.method == 'POST':
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                sys.stderr.write("*** file_upload *** aaa ***\n")
                handle_uploaded_file(request.FILES['file'])
                file_obj = request.FILES['file']
                sys.stderr.write(file_obj.name + "\n")
                messages.add_message(request, messages.INFO, 'インポートされました。')
                return redirect('office')
        else:
            offices = Office.objects.all()
            form = UploadFileForm()
            last_update_at = getLastUpdateAt('office')
        context = addTmcAuth({'form': form, 'offices': offices,
                             'last_update_at': last_update_at, }, request.user)
        return render(request, 'offices/upload.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'この権限では許可されていません。')
    return redirect('office')


def handle_uploaded_file(file_obj):
    sys.stderr.write("*** handle_uploaded_file *** aaa ***\n")
    sys.stderr.write(file_obj.name + "\n")
    file_path = 'uploads/documents/Offices.csv'
    sys.stderr.write(file_path + "\n")
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            sys.stderr.write("*** handle_uploaded_file *** ccc ***\n")
            destination.write(chunk)
            sys.stderr.write("*** handle_uploaded_file *** eee ***\n")
    offices_csv_import()
