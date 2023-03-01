import imp
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render

import sys

from .forms import UploadFileForm, OfficeCreateForm
from .models import Office, offices_csv_import
from accounts.views import addIsStaff
from histories.models import getLastUpdateAt


@login_required
def office_del(request, office_id):
    if request.user.is_staff:
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
    if request.user.is_staff:
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
        context = addIsStaff({'form': form, 'offices': offices,
                             'last_update_at': last_update_at, }, request.user)
        return render(request, 'offices/upload.html', context)
    else:
        messages.add_message(request, messages.WARNING, 'この権限では許可されていません。')
    return redirect('office')


def api_posts_get(request):
    """サジェスト候補の記事をJSONで返す。"""
    keyword = request.GET.get('keyword').upper()
    if keyword:
        office_list = [{'pk': office.pk, 'name': str(office)} for office in Office.objects.filter(
            Q(id__contains=keyword) | Q(name__contains=keyword))]
    else:
        office_list = []
    return JsonResponse({'object_list': office_list})


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


@login_required
def file_downnload(request):
    return FileResponse(open('uploads/documents/Offices.csv', 'rb'), filename='office.csv', as_attachment=True)

@login_required
def office_new(request):
    if not request.user.is_staff:
        messages.add_message(request, messages.ERROR, 'この権限では許可されていません。')
        return redirect('top')
    if request.method == 'POST':
        id = request.POST.get('id')
        unyo_sts = request.POST.get('unyo_sts')
        name = request.POST.get('name')
        shortcut_name = request.POST.get('shortcut_name')
        flg = True
        if len(id) > 4:
            messages.add_message(request, messages.ERROR, '官署コードは4文字以内')
            flg = False
        office = Office.objects.get_or_none(id=id)
        if office:
            messages.add_message(request, messages.ERROR, '当該官署は既に登録されています')
            flg = False
        if flg:
            office = Office.objects.create(id=id)
            office.unyo_sts = (unyo_sts == 'on')
            office.name = name
            office.shortcut_name = shortcut_name
            office.save()
            messages.add_message(request, messages.INFO, '登録されました')
        return redirect('office')
    else:
        form = OfficeCreateForm()
        context = addIsStaff({'form': form}, request.user)
    return render(request, "offices/officeNew.html", context)
