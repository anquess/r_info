from django.db import models
from django.http import Http404

from datetime import datetime as dt

def csvFormatCheck(csvRow, checkLists) -> bool:
    for check in checkLists:
        if not check in csvRow:
            raise Http404('CSVデータに項目%sがありません' % check)
    return True

def getSysupdtime(row) -> dt:
    if row['DATASHUSEI_DATE']:
        sysupdtime = dt.strptime(row['DATASHUSEI_DATE'], '%Y/%m/%d %H:%M:%S')
    else:
        sysupdtime = dt.strptime(row['SYSUPDTIME'], '%Y/%m/%d %H:%M:%S')
    return sysupdtime

class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        """
        検索にヒットすればそのモデルを、しなければNoneを返します。
        """
        try:
            return self.get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            return None
