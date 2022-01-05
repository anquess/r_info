from django.core.exceptions import ValidationError

def csvFormatCheck(csvRow, checkLists):
    for check in checkLists:
        if not check in csvRow:
            raise ValidationError(
                'CSVデータに項目がありません : %s' % check,
                code='invalid')
