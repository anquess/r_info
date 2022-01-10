from django import forms
from django.http import Http404

import csv

from rise_info.baseForms import csvFormatCheck

def formatCheck(eqtypes):
    csvFormatCheck(
        eqtypes, ('SOCHIKATA', 'DATASAKUSEI_DATE', ))

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='EQType.csvファイル',
        help_text='RISE/APPS 専用エクスポートツール(Access or Excel)で抽出したデータのみ',
        required=True,
        widget=forms.widgets.FileInput(
            attrs={
                'class': 'form-control',
            },       
        )
    )
    def clean_file(self):
        file = self.cleaned_data['file']
        with open('uploads/documents/EQTypes.csv', 'rt', encoding = "utf-8-sig") as f:
            reader = csv.reader(f)
            header = reader.__next__()
            try:
                formatCheck(header)
            except Exception as e:
                raise Http404(e, str(header))
        return file