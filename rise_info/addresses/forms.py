from django import forms
from django.urls import reverse_lazy

from .models import Addresses
from offices.widgets import OfficeSuggestWidget


class AddressesForm(forms.ModelForm):
    class Meta:
        model = Addresses
        fields = (
            'name',
            'position',
            'mail',
            'is_required_when_send_mail',
            'department',
            'offices',
            'offices_groups',
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
            'name': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
            }),
            'position': forms.TextInput(attrs={
                'type': 'text',
                'class': 'form-control',
            }),
            'mail': forms.EmailInput(attrs={
                'type': 'mail',
                'class': 'form-control',
            }),
            'offices': OfficeSuggestWidget(attrs={
                'data-url': reverse_lazy('api_posts_get')
            }),
            'offices_groups': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            }),
            'department': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'mutiple': True,
            })
        }
