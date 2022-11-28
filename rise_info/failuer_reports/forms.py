from django import forms
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError


from .models import FailuerReport, AttachmentFile, Circumstances
from rise_info.baseForms import MetaCommonInfo
from offices.widgets import OfficeSuggestWidget
from offices.models import Office


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
    def __init__(self, *args, **kwd):
        super(FailuerReportForm, self).__init__(*args, **kwd)
        self.fields["failuer_date"].required = True
        self.fields["failuer_time"].required = True
        self.fields["date_time_confirmation"].required = True
        self.fields["failuer_place"].required = True
        self.fields["eq"].required = True
        self.fields["sammary"].required = True

    def clean_offices(self):
        offices = self.cleaned_data['offices']
        if len(offices) == 0:
            raise ValidationError(
                code='offices', message='関係官署は配信先の判定に使用するため必須です')
        return offices

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
            'offices',
            'eq',
            'department',
            'sammary',
            'recovery_propects',
            'is_operatinal_impact',
            'operatinal_impact',
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
            'operatinal_impact': {
                'max_length': '運用への影響は128文字以内です',
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
                'class': 'form-control',
            }),
            'failuer_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
            'date_time_confirmation': forms.widgets.Select(attrs={
                "class": "form-select",
                "aria-describedby": "confirmationHelp",
            }),
            'failuer_place': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder": '障害発生場所(必須)',
            }),
            'offices':  OfficeSuggestWidget(
                attrs={'data-url': reverse_lazy('api_posts_get')
                       }),
            'eq': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
                "placeholder": '障害装置(必須)',
            }),
            'department': forms.SelectMultiple(attrs={
                'class': 'form-control',
            }),
            'sammary': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
                "placeholder": '障害概要(必須)',
            }),
            'recovery_propects': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": '復旧の見通し(必須)',
                "rows": "3",
            }),
            'is_operatinal_impact': forms.widgets.Select(attrs={
                "class": "form-select"
            }),
            'operatinal_impact': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": '運用への影響',
            }),
            'is_flight_impact': forms.widgets.Select(attrs={
                "class": "form-select"
            }),
            'flight_impact': forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": '運航への影響',
            }),
            'notam': forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": 'ノータム内容',
                "rows": "1",
            }),
            'is_press': forms.widgets.Select(attrs={
                "class": "form-select"
            }),
            'press_contents': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "1",
                "placeholder": "取材の内容",
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
                "placeholder": "備考",
            })
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
            'class': 'form-control',
        }),
        'time': forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control',
        }),
        'event': forms.Textarea(attrs={
            "class": "form-control",
            "rows": "2",
            "placeholder": "日付、時間が入った行は必須(256文字以内)",
        }),
    }
)
