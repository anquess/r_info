from django import forms

from infos.models import Info, InfoFile

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('title', 'sammary', 'is_rich_text', 'content')

FileFormSet = forms.inlineformset_factory(
    Info, InfoFile, fields='__all__', extra=1,
)