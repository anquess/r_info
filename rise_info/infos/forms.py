from django import forms
from django.forms import widgets

from infos.models import Info, AttachmentFile
from rise_info.baseForms import MetaCommonInfo

class InfoForm(forms.ModelForm):
    class Meta(MetaCommonInfo):
        model = Info
        fields = MetaCommonInfo.fields + ('info_type', 'managerID', 'sammary', 'is_rich_text')
        error_messages = {
            'managerID': {
                'required': '管理番号は必須です',
                'max_length': '管理番号は32文字以内です。'
            },
            'sammary': {
                'max_length': '概要への影響は512文字以内です',
            },
        }
        widgets = {**MetaCommonInfo.widgets, **{
            'info_type': forms.widgets.Select(attrs={
                "class": "form-select",
            }),
            'managerID': forms.TextInput(attrs={
                "class": "form-control",
            }),
            'sammary': forms.Textarea(attrs={
                "class": "form-control",
                "rows":"3",
            }),
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
        }}
FileFormSet = forms.inlineformset_factory(
    Info, AttachmentFile, fields='__all__', extra=1,
)