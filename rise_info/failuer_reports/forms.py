from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


from .models import FailuerReport, AttachmentFile, Circumstances
from rise_info.baseForms import MetaCommonInfo


class IsNullValidator:
    def __init__(self, attr_name: str, attr_jpn_name: str) -> None:
        self._attr_name = attr_name
        self._err_message = f"{attr_jpn_name}は最低でも1つ必要です"

    def __call__(self, attr):
        if len(attr) == 0:
            raise ValidationError(
                code='attr_count',
                message=self._err_message
            )


class FailuerReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            if key.startswith('is') or key == 'date_time_confirmation' or key.startswith('select'):
                value.widget.attrs['class'] = 'form-select'
            else:
                value.widget.attrs['class'] = 'form-control'

        self.fields["failuer_date"].required = True
        self.fields["failuer_time"].required = True
        self.fields["date_time_confirmation"].required = True
        self.fields["failuer_place"].required = True
        self.fields["eq"].required = True
        self.fields["sammary"].required = True

    def clean_department(self):
        department = self.cleaned_data['department']
        if len(department) == 0:
            raise ValidationError(
                code='department', message='関係装置分類は配信先の判定に使用するため必須です')
        return department

    class Meta(MetaCommonInfo):
        model = FailuerReport
        fields = MetaCommonInfo.fields + (
            'failuer_date',
            'failuer_time',
            'date_time_confirmation',
            'failuer_place',
            'eq',
            'department',
            'sammary',
            'recovery_date',
            'recovery_time',
            'recovery_propects',
            'is_flight_impact',
            'flight_impact',
            'notam',
            'is_press',
            'press_contents',
        )
        error_messages = {
            'failuer_date': {
                'required': '障害発生日は必須です',
            },
            'failuer_time': {
                'required': '障害発生時間は必須です',
            },
            'date_time_confirmation': {
                'required': '発生日時確認状態は必須です',
            },
            'failuer_place': {
                'required': '障害発生場所は必須です',
                'max_length': '障害発生場所は32文字以内です。',
            },
            'eq': {
                'required': '障害装置は必須です',
                'max_length': '障害装置は32文字以内です。',
            },
            'sammary': {
                'required': '障害状況は必須です',
                'max_length': '障害状況は512文字以内です。'
            },
            'recovery_propects': {
                'required': '復旧の見通しは必須です',
                'max_length': '復旧の見通しは1024文字以内です。'
            },
            'flight_impact': {
                'max_length': '運航への影響は128文字以内です',
            },
            'notam': {
                'max_length': 'ノータムは512文字以内です',
                'rows': 3,
            },
            'press_contents': {
                'max_length': '取材の内容は1024文字以内です',
            },
            'content': {
                'max_length': '備考は4096文字以内です',
            },
        }
        widgets = {**MetaCommonInfo.widgets, **{
            'failuer_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'failuer_time': forms.TimeInput(attrs={
                'type': 'time',
            }),
            'date_time_confirmation': forms.widgets.Select(attrs={
                "aria-describedby": "confirmationHelp",
            }),
            'sammary': forms.Textarea(attrs={
                "rows": "3",
            }),
            'recovery_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'recovery_time': forms.TimeInput(attrs={
                'type': 'time',
            }),
            'recovery_propects': forms.Textarea(attrs={
                "rows": "3",
            }),
            'is_flight_impact': forms.widgets.Select(),
            'notam': forms.Textarea(attrs={
                "rows": "3",
            }),
            'is_press': forms.widgets.Select(),
            'press_contents': forms.Textarea(attrs={
                "rows": "3",
            }),
            "content": forms.Textarea(attrs={
                "rows": "3",
            })
        }}


class CircumstancesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            if key != 'delete':
                value.widget.attrs['placeholder'] = value.help_text
                value.widget.attrs['class'] = 'form-control'

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
                'max_length': '事象は256文字以内です。',
                'type': 'date',
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
        }),
        'time': forms.TimeInput(attrs={
            'type': 'time',
        }),
        'event': forms.Textarea(attrs={
            "rows": "2",
        }),
    }
)
