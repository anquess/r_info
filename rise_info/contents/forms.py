from django import forms

from contents.models import Contents, AttachmentFile
from rise_info.baseForms import MetaCommonInfo


class ContentsForm(forms.ModelForm):
    class Meta(MetaCommonInfo):
        model = Contents
        fields = MetaCommonInfo.fields + ('is_rich_text',)
        widgets = {**MetaCommonInfo.widgets, **{
            'is_rich_text': forms.CheckboxInput(attrs={
                'onclick': 'simplemde = makeSimplemde(this.checked)',
            }),
        }}


FileFormSet = forms.inlineformset_factory(
    Contents, AttachmentFile, fields='__all__', extra=1,
)
