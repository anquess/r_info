from django import forms
from django.http import Http404

import csv

from rise_info.baseForms import csvFormatCheck
from .models import Office

def formatCheck(offices):
    csvFormatCheck(
        offices, (
            'KANSHO_CD',
            'UNYOSTS_KBN',
            'KANSHO_NM',
            'KANSHO_SNM',
            'DATASHUSEI_DATE',
            'SYSUPDTIME',
        )
    )


class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'
    file = forms.FileField(
        label='Office.csvファイル',
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
        with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
            reader = csv.reader(f)
            header = reader.__next__()
            try:
                formatCheck(header)
            except Exception as e:
                raise Http404(e, str(header))
        return file

class OfficeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            if key != 'unyo_sts':
                value.widget.attrs['class'] = 'form-control'
            else:
                value.widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Office
        fields = ('unyo_sts', 'name', 'shortcut_name')
