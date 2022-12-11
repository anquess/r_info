from django import forms
from django.urls import reverse_lazy

from infos.models import Info, AttachmentFile, InfoComments
from rise_info.baseForms import MetaCommonInfo, FileSizeValidator
from eqs.widgets import SuggestWidget
from offices.widgets import OfficeSuggestWidget


class InfoCommentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'

    info = forms.ModelChoiceField(
        queryset=Info.objects.all(),
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
        model = InfoComments
        fields = ('info', 'file', 'comment_txt')
        widgets = {
            "comment_txt": forms.Textarea(),
            "file": forms.FileInput(),
        }


class InfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            if key != 'offices' and key != 'eqtypes' and not key.startswith('is_'):
                value.widget.attrs['placeholder'] = value.help_text
                if key == 'info_type':
                    value.widget.attrs['class'] = 'form-select'
                else:
                    value.widget.attrs['class'] = 'form-control'

    class Meta(MetaCommonInfo):
        model = Info
        fields = MetaCommonInfo.fields + \
            ('info_type', 'managerID', 'sammary', 'is_rich_text', 'is_add_eqtypes',
             'is_add_offices', 'eqtypes', 'offices', 'is_disclosed', 'disclosure_date')
        error_messages = {**MetaCommonInfo.error_messages, **{
            'info_type': {
                'required': '情報種別は必須です',
            },
            'managerID': {
                'required': '管理番号は必須です',
                'max_length': '管理番号は32文字以内です'
            },
            'sammary': {
                'max_length': '概要は512文字以内です',
            },
            'disclosure_date': {
                'required': '公開日は必須です',
            },
        }}
        widgets = {**MetaCommonInfo.widgets, **{
            'info_type': forms.widgets.Select(),
            'managerID': forms.TextInput(),
            'sammary': forms.Textarea(attrs={
                "rows": "3",
            }),
            'is_add_offices': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "offices-input", true)',
            }),
            'is_add_eqtypes': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "eqtypes-input", true)',
            }),
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
            'is_disclosed': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_disclosure_date", false)',
            }),
            'disclosure_date': forms.DateInput(attrs={
                'type': 'date',
            }),
            'eqtypes': SuggestWidget(
                attrs={'data-url': reverse_lazy('eqs:api_posts_get')}),
            'offices': OfficeSuggestWidget(attrs={'data-url': reverse_lazy('api_posts_get')}),
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
    Info, AttachmentFile, form=AttachmentFileForm, fields='__all__', extra=1,
)
