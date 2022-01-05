from django import forms

from .models import FailuerReport, AttachmentFile
from rise_info.baseForms import MetaCommonInfo

class FailuerReportForm(forms.ModelForm):
    class Meta(MetaCommonInfo):
        model = FailuerReport
        fields = MetaCommonInfo.fields + (
            'sammary',
            'is_operatinal_impact',
            'operatinal_impact',
            'is_flight_impact',
            'flight_impact',
             )
FileFormSet = forms.inlineformset_factory(
    FailuerReport, AttachmentFile, fields='__all__', extra=1,
)