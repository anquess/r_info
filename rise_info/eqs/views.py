from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import sys

from .forms import UploadFileForm
from .models import Eqtype, eqtypes_csv_import
from .serializer import EqtypeSerializer
from accounts.views import isInTmcGroup, addTmcAuth
from histories.models import getLastUpdateAt

@login_required
def eqtype_del(request, slug):
    try:
        if isInTmcGroup(request.user):
            for eqtype in Eqtype.objects.filter(slug=slug):
                eqtype.delete()
                messages.add_message(request, messages.INFO, f"{eqtype.id}は削除されました")    
        else:
            messages.add_message(request, messages.ERROR, "この権限では許可されていません。")
    except Exception as e:
        messages.add_message(request, messages.ERROR, str(e))    

    return redirect('eqtype')

@api_view(['GET'])
def get_eqtypes_json(request):
    if request.method == 'GET':
        eqtypes = Eqtype.objects.all()
        serializers = EqtypeSerializer(eqtypes, many=True)
        return Response(serializers.data)


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
                messages.add_message(request, messages.INFO, '登録されました')
        else:            
            eqtypes = Eqtype.objects.all()
            form = UploadFileForm()
            last_update_at = getLastUpdateAt('eqtype')
        try:
            context = addTmcAuth({'form': form, 'eqtypes': eqtypes, 'last_update_at': last_update_at, }, request.user)
            return render(request, 'eqs/eqtypes/upload.html', context)
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'予期せぬエラーが発生しました。 エラーメッセージ:{str(e)}')
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