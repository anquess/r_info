from django import forms

from .models import FailuerReport

class FailuerReportForm(forms.ModelForm):
    class Meta:
        model = FailuerReport
        fields = ('title', 'sammary', 'content')