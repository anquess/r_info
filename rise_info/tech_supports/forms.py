from django import forms
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy

from .models import AttachmentFile, TechSupportComments, TechSupportsRelation, TechSupports
from rise_info.baseForms import MetaCommonInfo, FileSizeValidator
from eqs.widgets import SuggestWidget


class TechSupportCommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'
    info = forms.ModelChoiceField(
        queryset=TechSupports.objects.all(),
        error_messages={'required': 'infoは必須です', },
    )
    comment_txt = forms.CharField(
        required=True,
        max_length=512,
        error_messages={
            'max_length': 'コメントは512文字以内です',
            'required': 'コメントは必須です',
        },
    )
    file = forms.FileField(
        validators=[FileSizeValidator(val=10, byte_type="mb")],
        required=False,
    )

    class Meta:
        model = TechSupportComments
        fields = ('info', 'file', 'comment_txt')
        widgets = {
            "comment_txt": forms.Textarea(attrs={
                "class": "form-control",
            }),
            "file": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }


class TechSupportsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            if key != 'eqtypes' and not key.startswith('is_'):
                value.widget.attrs['placeholder'] = value.help_text
                if key == 'info_type' or key.startswith('select'):
                    value.widget.attrs['class'] = 'form-select'
                else:
                    value.widget.attrs['class'] = 'form-control'

    def clean_eqtypes(self):
        eqtypes = self.cleaned_data['eqtypes']
        if len(eqtypes) == 0:
            raise ValidationError(
                code='eqtypes', message='装置型式は必須です')
        return eqtypes

    class Meta(MetaCommonInfo):
        model = TechSupportsRelation
        fields = MetaCommonInfo.fields + \
            ('info_type', 'inquiry', 'is_rich_text', 'eqtypes')
        error_messages = {**MetaCommonInfo.error_messages, **{
            'info_type': {
                'required': '情報種別は必須です',
            },
            'inquiry': {
                'max_length': '概要は2048文字以内です',
            },
        }}
        widgets = {**MetaCommonInfo.widgets, **{
            'info_type': forms.widgets.Select(),
            'inquiry': forms.Textarea(attrs={
                "rows": "3",
            }),
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
            'eqtypes': SuggestWidget(attrs={
                'data-url': reverse_lazy('eqs:api_posts_get')
            }),
            "select_register": forms.TextInput(attrs={
                "type": "hidden",
                "value": "temporaty",
            })

        }}


class AttachmentFileForm(forms.ModelForm):
    file = forms.FileField(
        validators=[FileSizeValidator(val=100, byte_type="mb")],
        required=True,
    )

    class Meta(MetaCommonInfo):
        model = AttachmentFile
        fields = '__all__'


FileFormSet = forms.inlineformset_factory(
    TechSupportsRelation, AttachmentFile, form=AttachmentFileForm, fields='__all__', extra=1,
)
