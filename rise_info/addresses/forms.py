from django import forms

from .models import Addresses


class AddressesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            if key != 'is_HTML_mail':
                value.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Addresses
        fields = (
            'name',
            'position',
            'mail',
            'is_HTML_mail',
            'role',
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
            'is_HTML_mail': forms.CheckboxInput(),
            'role': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            }),
            'group': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            }),
            'department': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            }),
        }
