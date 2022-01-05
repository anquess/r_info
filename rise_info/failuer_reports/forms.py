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
        widgets = {**MetaCommonInfo.widgets, **{
            'sammary': forms.Textarea(attrs={
                "class": "form-control",
                "rows":"3",
            }),
            'is_operatinal_impact':forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_operatinal_impact")',
            }),
            'is_flight_impact': forms.CheckboxInput(attrs={
                'onclick': 'clickCheck(this.id, "id_flight_impact")',
            }),

        }}
FileFormSet = forms.inlineformset_factory(
    FailuerReport, AttachmentFile, fields='__all__', extra=1,
)