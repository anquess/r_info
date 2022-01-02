from django import forms
from django.db.models import fields

from infos.models import Info, InfoAttachmentFile

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('title', 'sammary', 'is_rich_text', 'content')

FileFormSet = forms.inlineformset_factory(
    Info, InfoAttachmentFile, fields='__all__', extra=1,
)