from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


from .models import FailuerReportRelation, AttachmentFile, Circumstances
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


class FailuerReportRelationForm(forms.ModelForm):
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
        model = FailuerReportRelation
        fields = MetaCommonInfo.fields + (
            'failuer_date',
            'failuer_time',
            'date_time_confirmation',
            'failuer_place',
            'eq',
            'department',
            'sammary',
            'cause',
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
                'max_length': '障害発生場所は128文字以内です。',
            },
            'eq': {
                'required': '障害装置は必須です',
                'max_length': '障害装置は128文字以内です。',
            },
            'sammary': {
                'required': '障害概要は必須です',
                'max_length': '障害概要は1024文字以内です。'
            },
            'cause': {
                'required': '障害原因は必須です',
                'max_length': '障害原因は1024文字以内です。'
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
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "bottom",
                "title": "必須項目\n何がどうなったか簡潔に\n例:LOC が●●ALM発生により停止",
                "rows": "3",
            }),
            'cause': forms.Textarea(attrs={
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "bottom",
                "title": "必須項目\n現時点で判明している事柄を記載\n例:詳細確認中",
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
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "bottom",
                "title": "必須項目\n分かる範囲で予定等を記載\n例:保守員の派遣を調整中"
            }),
            'is_flight_impact': forms.widgets.Select(),
            'notam': forms.Textarea(attrs={
                "rows": "3",
            }),
            'flight_impact': forms.Textarea(attrs={
                "rows": "3",
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "bottom",
                "title": "現時点で判明している事柄を記載\n例:確認中"
            }),
            'is_press': forms.widgets.Select(),
            'press_contents': forms.Textarea(attrs={
                "rows": "3",
                "data-bs-toggle": "tooltip",
                "data-bs-placement": "bottom",
                "title": "有の場合はその概要\n\
施設障害時の取材対応やプレス発表時における現地官署の対応については、以下を基本とする。\n\
①基本的に、発生事案については、全ての事項を本省管技課で対応\n\
②官署への取材等が行われる場合を想定し、関係官署の広報担当者に答弁ラインを連絡するとともに、\n\
　当該官署における広報対応の体制について確認（答弁は当該官署の広報担当にて実施。）\n\
③現地官署での取材内容は、本省管制技術課危機管理担当に逐次報告"
            }),
            "content": forms.Textarea(attrs={
                "rows": "3",
            }),
            "select_register": forms.TextInput(attrs={
                "type": "hidden",
                "value": "temporaty",
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
    FailuerReportRelation, AttachmentFile, fields='__all__', extra=1,
)
CircumstancesFormSet = forms.inlineformset_factory(
    FailuerReportRelation, Circumstances, fields='__all__', extra=1,
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
