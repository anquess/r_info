from django import forms

import csv

from rise_info.baseForms import csvFormatCheck

def formatCheck(offices):
    csvFormatCheck(
        offices, (
            'KANSHO_CD',
            'KANSHO_NM',
            'KANSHO_SNM',
            'DATASHUSEI_DATE',
            'SYSUPDTIME',
            )
        )


class UploadFileForm(forms.Form):
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
            reader = csv.DictReader(f)
            formatCheck(reader[0])
        return file