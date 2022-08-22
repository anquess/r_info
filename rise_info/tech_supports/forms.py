from django import forms
from django.urls import reverse_lazy

from .models import TechSupports, AttachmentFile, TechSupportComments
from rise_info.baseForms import MetaCommonInfo, FileSizeValidator
from eqs.widgets import SuggestWidget
from offices.widgets import OfficeSuggestWidget


class TechSupportCommentsForm(forms.ModelForm):
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
    class Meta(MetaCommonInfo):
        model = TechSupports
        fields = MetaCommonInfo.fields + \
            ('inquiry', 'is_rich_text', 'eqtypes', 'is_closed')
        error_messages = {**MetaCommonInfo.error_messages, **{
            'inquiry': {
                'max_length': '概要は2048文字以内です',
            },
        }}
        widgets = {**MetaCommonInfo.widgets, **{
            'inquiry': forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
            }),
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
            'is_closed': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_disclosure_date", false)',
            }),
            'eqtypes': SuggestWidget(attrs={'data-url': reverse_lazy('eqs:api_posts_get')}),
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
    TechSupports, AttachmentFile, form=AttachmentFileForm, fields='__all__', extra=1,
)
