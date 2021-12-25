from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render

import sys

from .forms import UploadFileForm
from .models import Office, offices_csv_import
from accounts.views import isInTmcGroup, addTmcAuth

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
                return HttpResponseRedirect('/')
        else:
            offices = Office.objects.all()
            form = UploadFileForm()
        context = addTmcAuth({'form': form, 'offices': offices }, request.user)
        return render(request, 'offices/upload.html', context)
    else:
        raise Http404("この権限では許可されていません。")

def handle_uploaded_file(file_obj):
    sys.stderr.write("*** handle_uploaded_file *** aaa ***\n")
    sys.stderr.write(file_obj.name + "\n")
    file_path = 'uploads/documents/' + "Offices.csv" 
    sys.stderr.write(file_path + "\n")
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            sys.stderr.write("*** handle_uploaded_file *** ccc ***\n")
            destination.write(chunk)
            sys.stderr.write("*** handle_uploaded_file *** eee ***\n")
    offices_csv_import()