from django import forms

from infos.models import Info, AttachmentFile

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('title', 'sammary', 'is_rich_text', 'content')

FileFormSet = forms.inlineformset_factory(
    Info, AttachmentFile, fields='__all__', extra=1,
)