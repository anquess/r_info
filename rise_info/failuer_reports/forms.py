from django import forms

from .models import FailuerReport

class FailuerReportForm(forms.ModelForm):
    class Meta:
        model = FailuerReport
        fields = (
            'title',
            'sammary',
            'content', 
            'is_operatinal_impact',
            'operatinal_impact',
            'is_flight_impact',
            'flight_impact',
             )