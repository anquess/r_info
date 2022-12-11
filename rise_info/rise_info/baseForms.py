from dataclasses import field
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

from rise_info.baseModels import CommonInfo, BaseCommnets


class FileSizeValidator:
    def __init__(self, val: float, byte_type="mb"):
        assert byte_type in ["b", "kb", "mb", "gb"]
        if byte_type == "b":
            self._upper_byte_size = val
        elif byte_type == "kb":
            self._upper_byte_size = 1000 * val
        elif byte_type == "mb":
            self._upper_byte_size = (1000 ** 2) * val
        elif byte_type == "gb":
            self._upper_byte_size = (1000 ** 3) * val
        self._err_message = f"アップロードファイルは{val}{byte_type.upper()}未満にしてください"

    def __call__(self, file_val: UploadedFile):
        byte_size = file_val.size
        if byte_size > self._upper_byte_size:
            raise ValidationError(
                code='file',
                message=self._err_message
            )


def csvFormatCheck(csvRow, checkLists):
    for check in checkLists:
        if check not in csvRow:
            raise ValidationError(
                'CSVデータに項目がありません : %s' % check,
                code='invalid')


class MetaCommonInfo:
    model = CommonInfo
    fields = ('title', 'content', 'select_register')
    widgets = {
        "title": forms.TextInput(attrs={
            "aria-label": "運用への影響",

        }),
        "content": forms.Textarea(attrs={
        })
    }
    error_messages = {
        'title': {
            'required': 'タイトルは必須です',
            'max_length': 'タイトルは128文字以内です',
        },
        'content': {
            'max_length': '内容は4096文字以内です',
        },
    }
