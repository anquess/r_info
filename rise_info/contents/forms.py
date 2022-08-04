from django import forms

from contents.models import Contents, AttachmentFile, Menu, ContentComments
from rise_info.baseForms import MetaCommonInfo, FileSizeValidator


class ContentCommentsForm(forms.ModelForm):
    content = forms.ModelChoiceField(
        queryset=Contents.objects.all(),
        error_messages={'required': 'contentは必須です', },
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
        model = ContentComments
        fields = ('content', 'file', 'comment_txt')
        widgets = {
            "comment_txt": forms.Textarea(attrs={
                "class": "form-control",
            }),
            "file": forms.FileInput(attrs={
                "class": "form-control",
            }),
        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('menu_title', )


class ContentsForm(forms.ModelForm):
    class Meta(MetaCommonInfo):
        model = Contents
        fields = MetaCommonInfo.fields + ('is_rich_text', 'menu',)
        error_messages = {**MetaCommonInfo.error_messages, **{
            'menu': {
                'required': 'メニューは必須です',
            },
        }}

        widgets = {**MetaCommonInfo.widgets, **{
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
            'menu': forms.Select(attrs={
                "class": "form-control",
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
    Contents, AttachmentFile, form=AttachmentFileForm, fields='__all__', extra=1,
)
