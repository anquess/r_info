from django import forms
from django.core.exceptions import ValidationError

from .models import FailuerReport, AttachmentFile, Circumstances
from rise_info.baseForms import MetaCommonInfo

class FailuerReportForm(forms.ModelForm):
    class Meta(MetaCommonInfo):
        model = FailuerReport
        fields = MetaCommonInfo.fields + (
            'sammary',
            'is_operatinal_impact',
            'operatinal_impact',
            'is_flight_impact',
            'flight_impact',
             )
        error_messages = {
            'sammary': {
                'max_length': '概要は512文字以内です。'
            },
            'operatinal_impact': {
                'max_length': '運用への影響は128文字以内です',
            },
            'flight_impact': {
                'max_length': '運航への影響は128文字以内です',
            },
        }
        widgets = {**MetaCommonInfo.widgets, **{
            'sammary': forms.Textarea(attrs={
                "class": "form-control",
                "rows":"3",
            }),
            'is_operatinal_impact':forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_operatinal_impact")',
            }),
            'is_flight_impact': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_flight_impact")',
            }),
        }}

class CircumstancesForm(forms.ModelForm):
    class Meta:
        model = Circumstances
        fields = '__all__'
        labels = {
            'info': '情報',
            'date': '日付',
            'time': '時間',
            'event': '事象',
            'id': 'ID',
            'delete': '削除',
        }
        error_messages = {
            'event': {
                'required': '事象は必須です',
                'max_length': '事象は256文字以内です。'
            },
        }

FileFormSet = forms.inlineformset_factory(
    FailuerReport, AttachmentFile, fields='__all__', extra=1,
)
CircumstancesFormSet= forms.inlineformset_factory(
    FailuerReport, Circumstances, fields='__all__', extra=1, form=CircumstancesForm,
    widgets={
        'date': forms.DateInput(attrs={
            'class': 'form-control',
            'onclick': "$(this).not('.hasDatePicker').datepicker();$(this).datepicker('show')",
        }),
        'time': forms.TimeInput(attrs={
            'class': 'form-control',
        }),
        'event': forms.Textarea(attrs={
            'class': 'form-control',
            'rows':'2',
        }),
    }
)