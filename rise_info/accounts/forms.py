from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import User_mail_config


class MyPasswordChangeForm(PasswordChangeForm):
    """パスワード変更フォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'


class UserAddForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text
            value.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'password1', 'password2', 'groups')


class UserMailConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserMailConfigForm, self).__init__(*args, **kwargs)
        for _, value in self.fields.items():
            value.widget.attrs['placeholder'] = value.help_text

    class Meta:
        model = User_mail_config
        fields = ('user', 'email_address',
                  'default_email_header', 'default_email_footer')
        error_messages = {
            "default_email_header": {
                "max_length": 'デフォルト送信時メールヘッダーは512文字以内'
            },
            "default_email_footer": {
                "max_length": 'デフォルト送信時メールフッターは512文字以内'
            }
        }
        widgets = {
            "user": forms.Select(),
            "email_address": forms.EmailInput(),
            "default_email_header": forms.Textarea(attrs={
                "rows": 3,
            }),
            "default_email_footer": forms.Textarea(attrs={
                "rows": 3,
            }),

        }
