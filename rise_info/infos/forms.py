from django import forms
from django.urls import reverse_lazy

from infos.models import Info, AttachmentFile
from rise_info.baseForms import MetaCommonInfo
from eqs.widgets import SuggestWidget


class InfoForm(forms.ModelForm):
    class Meta(MetaCommonInfo):
        model = Info
        fields = MetaCommonInfo.fields + \
            ('info_type', 'managerID', 'sammary', 'is_rich_text',
             'eqtypes', 'is_disclosed', 'disclosure_date')
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
                "rows": "3",
            }),
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
            'is_disclosed': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_disclosure_date", false)',
            }),
            'disclosure_date': forms.DateInput(attrs={
                'class': 'form-control',
                'onclick': "$(this).not('.hasDatePicker').datepicker();$(this).datepicker('show')",
            }),
            'eqtypes': SuggestWidget(attrs={'data-url': reverse_lazy('eqs:api_posts_get')}),
        }}


FileFormSet = forms.inlineformset_factory(
    Info, AttachmentFile, fields='__all__', extra=1,
)
