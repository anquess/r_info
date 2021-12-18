from django import forms

from infos.models import Info

class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('title', 'sammary', 'content')