from django import forms
from django.urls import reverse_lazy

from .models import FailuerReport, AttachmentFile, Circumstances
from rise_info.baseForms import MetaCommonInfo
from offices.widgets import OfficeSuggestWidget


class FailuerReportForm(forms.ModelForm):
    def __init__(self, *args, **kwd):
        super(FailuerReportForm, self).__init__(*args, **kwd)
        self.fields["failuer_date"].required = True
        self.fields["failuer_time"].required = True
        self.fields["failuer_place"].required = True
        self.fields["date_time_confirmation"].required = True
        self.fields["sammary"].required = True

    class Meta(MetaCommonInfo):
        model = FailuerReport
        fields = MetaCommonInfo.fields + (
            'failuer_date',
            'failuer_time',
            'failuer_place',
            'date_time_confirmation',
            'offices',
            'recovery_propects',
            'is_press',
            'press_contents',
            'sammary',
            'is_operatinal_impact',
            'operatinal_impact',
            'is_flight_impact',
            'flight_impact',
        )
        error_messages = {
            'failuer_date': {
                'required': '障害発生日は必須です',
            },
            'failuer_time': {
                'required': '障害発生時間は必須です',
            },
            'failuer_place': {
                'required': '障害発生場所は必須です',
            },
            'date_time_confirmation': {
                'required': '発生日時確認状態は必須です',
            },
            'recovery_propects': {
                'max_length': '復旧の見通しは1024文字以内です。'
            },
            'sammary': {
                'required': '障害状況は必須です',
                'max_length': '障害状況は512文字以内です。'
            },
            'operatinal_impact': {
                'max_length': '運用への影響は128文字以内です',
            },
            'flight_impact': {
                'max_length': '運航への影響は128文字以内です',
            },
        }
        widgets = {**MetaCommonInfo.widgets, **{
            'failuer_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'failuer_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'failuer_place': forms.TimeInput(attrs={
                'type': 'text',
                'class': 'form-control',
            }),
            'date_time_confirmation': forms.widgets.Select(attrs={
                "class": "form-select",
                "aria-describedby": "confirmationHelp",
            }),
            'is_press': forms.widgets.Select(attrs={
                "class": "form-select"
            }),
            'offices': OfficeSuggestWidget(attrs={
                'data-url': reverse_lazy('api_posts_get')}),
            'sammary': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
            }),
            'recovery_propects': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
            }),
            'press_contents': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
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
CircumstancesFormSet = forms.inlineformset_factory(
    FailuerReport, Circumstances, fields='__all__', extra=1,
    form=CircumstancesForm,
    widgets={
        'date': forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        'time': forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        'event': forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '2',
        }),
    }
)
