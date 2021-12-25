from django.db import models
from django.http import Http404
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_authenticated_user)

from datetime import datetime as dt

from mdeditor.fields import MDTextField


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

class CommonInfo(models.Model):
    objects = BaseManager()
    title = models.CharField(verbose_name='タイトル', default="", null=False, blank=False, max_length=128)
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)
    content = MDTextField(verbose_name='内容', default="", null=False, blank=True)
    created_by = CurrentUserField(verbose_name='登録者',on_update=True, related_name='%(app_label)s_%(class)s_create', null=False, blank=False)
    created_at = models.DateTimeField(verbose_name='投稿日', auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True, null=False, blank=False)
    updated_by = CurrentUserField(verbose_name='更新者', on_update=True, related_name='%(app_label)s_%(class)s_update', null=False, blank=False)
    class Meta:
        abstract= True

    def __str__(self):
        return self.title
    
    def save(self,obj, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_authenticated_user()
        self.updated_by = get_current_authenticated_user()
        super(CommonInfo, self).save(*args, **kwargs)