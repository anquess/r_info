from django import forms

from .models import FailuerReport, AttachmentFile

class FailuerReportForm(forms.ModelForm):
    class Meta:
        model = FailuerReport
        fields = (
            'title',
            'sammary',
            'is_rich_text',
            'content', 
            'is_operatinal_impact',
            'operatinal_impact',
            'is_flight_impact',
            'flight_impact',
             )
FileFormSet = forms.inlineformset_factory(
    FailuerReport, AttachmentFile, fields='__all__', extra=1,
)