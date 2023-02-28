from django import forms
from django.http import Http404
from django.urls import reverse_lazy
from django.forms import ModelChoiceField
import csv

from .widgets import SuggestWidget
from .models import Eqtype, EQ_class
from rise_info.baseForms import csvFormatCheck


def formatCheck(eqtypes):
    csvFormatCheck(
        eqtypes, ('SOCHIKATA', 'DATASAKUSEI_DATE', ))


class EqTypeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs['class'] = 'form-select'

    #eq_class = ModelChoiceField(label="装置分類", queryset=EQ_class.objects.all())
    class Meta:
        model = Eqtype
        fields = ('eq_class',)
        widget = {
            'eq_class': forms.widgets.Select(attrs={
                "class":"form-select",
            })
        }




class UploadFileForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'
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
        with open('uploads/documents/EQTypes.csv', 'rt', encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            header = reader.__next__()
            try:
                formatCheck(header)
            except Exception as e:
                raise Http404(e, str(header))
        return file
