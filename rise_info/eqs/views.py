from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, FileResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
from django.utils.text import slugify

import sys

from .forms import UploadFileForm, EqTypeCreateForm, EqClassCreateForm
from .models import Eqtype, eqtypes_csv_import, EQ_class
from accounts.views import addIsStaff
from histories.models import getLastUpdateAt


@login_required
def eqtype_del(request, slug):
    try:
        if request.user.is_staff:
            for eqtype in Eqtype.objects.filter(slug=slug):
                eqtype.delete()
                messages.add_message(request, messages.INFO,
                                     f"{eqtype.id}は削除されました")
        else:
            messages.add_message(request, messages.ERROR, "この権限では許可されていません。")
    except Exception as e:
        messages.add_message(request, messages.ERROR, str(e))

    return redirect('eqs:eqtype')


def api_posts_get(request):
    """サジェスト候補の記事をJSONで返す。"""
    keyword = request.GET.get('keyword')
    if keyword:
        eqType_list = [{'pk': eqType.pk, 'name': str(
            eqType)} for eqType in Eqtype.objects.filter(id__icontains=keyword)]
    else:
        eqType_list = []
    return JsonResponse({'object_list': eqType_list})


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
                messages.add_message(request, messages.INFO, '登録されました')
        else:
            eqtypes = Eqtype.objects.all()
            form = UploadFileForm()
            last_update_at = getLastUpdateAt('eqtype')
        try:
            context = addIsStaff(
                {'form': form, 'eqtypes': eqtypes, 'last_update_at': last_update_at, }, request.user)
            return render(request, 'eqs/eqtypes/upload.html', context)
        except Exception as e:
            messages.add_message(request, messages.ERROR,
                                 f'予期せぬエラーが発生しました。 エラーメッセージ:{str(e)}')
    else:
        messages.add_message(request, messages.ERROR, 'この権限では許可されていません。')
    return HttpResponseRedirect('/eqs/eqtypes/')


def handle_uploaded_file(file_obj):
    sys.stderr.write("*** handle_uploaded_file *** aaa ***\n")
    sys.stderr.write(file_obj.name + "\n")
    file_path = 'uploads/documents/EQTypes.csv'
    sys.stderr.write(file_path + "\n")
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            sys.stderr.write("*** handle_uploaded_file *** ccc ***\n")
            destination.write(chunk)
            sys.stderr.write("*** handle_uploaded_file *** eee ***\n")
    eqtypes_csv_import()


@login_required
def file_downnload(request):
    return FileResponse(open('uploads/documents/EQTypes.csv', 'rb'), filename='EQTypes.csv', as_attachment=True)

@login_required
def eqtype_new(request):
    if not request.user.is_staff:
        messages.add_message(request, messages.ERROR, 'この権限では許可されていません。')
        return redirect('top')
    if request.method == 'POST':
        id = request.POST.get('id')
        slug = slugify(id)
        eq_class = request.POST.get('eq_class')
        flg = True
        if len(id) > 24:
            messages.add_message(request, messages.ERROR, '装置型式は24文字以内')
            flg = False
        eqtype = Eqtype.objects.get_or_none(id=id)
        if eqtype:
            messages.add_message(request, messages.ERROR, '当該装置型式は既に登録されています')
            flg = False
        if flg:
            eqtype = Eqtype.objects.create(id=id)
            eqtype.slug = slug
            eqtype.eq_class = eq_class
            eqtype.save()
            messages.add_message(request, messages.INFO, slug + 'は登録されました')

        return redirect('top')
    else:
        form = EqTypeCreateForm()
        context = addIsStaff({'form': form}, request.user)
    return render(request, "eqs/eqTypesNew.html", context)

@login_required
def eq_class_new(request):
    if not request.user.is_staff:
        messages.add_message(request, messages.ERROR, 'この権限では許可されていません。')
        return redirect('top')
    if request.method == 'POST':
        id = request.POST.get('id')
        departments = request.POST.getlist('department')
        memo = request.POST.get('memo')
        flg = True
        if len(id) > 16:
            messages.add_message(request, messages.ERROR, '装置分類は16文字以内')
            flg = False
        eq_class = EQ_class.objects.get_or_none(id=id)
        if eq_class:
            messages.add_message(request, messages.ERROR, '当該装置分類は既に登録されています')
            flg = False
        if flg:
            eq_class = EQ_class.objects.create(id=id)
            for department in departments:
                eq_class.department.add(department)
            eq_class.memo = memo
            eq_class.save()
            messages.add_message(request, messages.INFO, '登録されました')
        return redirect('eqs:eqtype_new')
    else:
        form = EqClassCreateForm()
        context = addIsStaff({'form': form}, request.user)
    return render(request, "eqs/eq_classNew.html", context)
