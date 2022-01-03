from django import forms

from infos.models import Info, AttachmentFile, InfoTypeChoices

#class InfoForm(forms.Form):
#    title = forms.CharField(label='タイトル', required=True, max_length=128)
#    info_type = forms.fields.ChoiceField(
#        label='情報種別',
#        choices=InfoTypeChoices,
#    )
#    managerID = forms.CharField(label='管理番号', initial='TMC-解析-', required=True, max_length=16)
#    sammary = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}), label='概要', max_length=512)
#    is_rich_text = forms.BooleanField(help_text='MD形式ならTrue', initial=False)
#    content = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}),label='詳細')
#    def save(self):
#        data = self.cleaned_data
#        info = Info(
#            title=data['title'],
#            info_type=data['info_type'],
#            managerID=data['managerID'],
#            sammary=data['sammary'],
#            is_rich_text=data['is_rich_text'],
#            content=data['content'],
#        )
#        info.save()
class InfoForm(forms.ModelForm):
    class Meta:
        model = Info
        fields = ('title','info_type', 'managerID', 'sammary', 'is_rich_text', 'content')

FileFormSet = forms.inlineformset_factory(
    Info, AttachmentFile, fields='__all__', extra=1,
)