from dataclasses import field
from django import forms
from django.core.exceptions import ValidationError

from rise_info.baseModels import CommonInfo, BaseCommnets


def csvFormatCheck(csvRow, checkLists):
    for check in checkLists:
        if check not in csvRow:
            raise ValidationError(
                'CSVデータに項目がありません : %s' % check,
                code='invalid')


class MetaCommonInfo:
    model = CommonInfo
    fields = ('title', 'content')
    widgets = {
        "title": forms.TextInput(attrs={
            "class": "form-control",
        }),
        "content": forms.Textarea(attrs={
            "class": "form-control",
        })
    }
