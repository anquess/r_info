from django import forms

from .models import Addresses


class AddressesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Addresses
        fields = (
            'name',
            'position',
            'mail',
            'groups',
            'department',
        )
        error_messages = {
            'name': {
                'required': '氏名は必須です',
                'max_length': '氏名は16文字以内です。'
            },
            'position': {
                'required': '役職は必須です',
                'max_length': '役職は16文字以内です。'
            },
            'mail': {
                'required': 'メールアドレスは必須です',
            },
        }
        widgets = {
            'name': forms.TextInput(),
            'position': forms.TextInput(),
            'mail': forms.EmailInput(),
            'group': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            }),
            'department': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            }),
        }
