from django import forms

from contents.models import ContentsRelation, AttachmentFile, Menu  # , ContentComments
from rise_info.baseForms import MetaCommonInfo, FileSizeValidator


# class ContentCommentsForm(forms.ModelForm):
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        for _, value in self.fields.items():
#            value.widget.attrs['placeholder'] = value.help_text
#            value.widget.attrs['class'] = 'form-control'
#
#    content = forms.ModelChoiceField(
#        queryset=ContentsRelation.objects.all(),
#        error_messages={'required': 'contentは必須です', },
#    )
#    comment_txt = forms.CharField(
#        required=True,
#        max_length=512,
#        error_messages={
#            'max_length': 'コメントは512文字以内です',
#            'required': 'コメントは必須です',
#        },
#    )
#    file = forms.FileField(
#        validators=[FileSizeValidator(val=10, byte_type="mb")],
#        required=False,
#    )
#
#    class Meta:
#        model = ContentComments
#        fields = ('content', 'file', 'comment_txt')
#        widgets = {
#            "comment_txt": forms.Textarea(attrs={
#                "class": "form-control",
#            }),
#            "file": forms.FileInput(attrs={
#                "class": "form-control",
#            }),
#        }


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ('menu_title', )


class ContentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            if not key.startswith('is_'):
                value.widget.attrs['placeholder'] = value.help_text
                if key == 'menu':
                    value.widget.attrs['class'] = 'form-select'
                else:
                    value.widget.attrs['class'] = 'form-control'

    class Meta(MetaCommonInfo):
        model = ContentsRelation
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
            'menu': forms.Select(),
            "select_register": forms.TextInput(attrs={
                "type": "hidden",
                "value": "not_registered",
            })
        }}


class AttachmentFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'

    file = forms.FileField(
        validators=[FileSizeValidator(val=100, byte_type="mb")],
        required=True,
    )

    class Meta(MetaCommonInfo):
        model = AttachmentFile
        fields = '__all__'


FileFormSet = forms.inlineformset_factory(
    ContentsRelation, AttachmentFile, form=AttachmentFileForm, fields='__all__', extra=1,
)
