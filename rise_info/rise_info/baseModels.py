from django.db import models
from django.http import Http404
from django.utils.safestring import mark_safe
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_authenticated_user)

from datetime import datetime as dt
import os
import shutil
import markdown

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
    content = models.TextField(verbose_name='内容', default="", null=False, blank=True)
    created_by = CurrentUserField(verbose_name='登録者',on_update=True, related_name='%(app_label)s_%(class)s_create', null=False, blank=False, max_length=4096)
    created_at = models.DateTimeField(verbose_name='投稿日', auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(verbose_name='更新日', auto_now=True, null=False, blank=False)
    updated_by = CurrentUserField(verbose_name='更新者', on_update=True, related_name='%(app_label)s_%(class)s_update', null=False, blank=False)
    class Meta:
        abstract= True

    def __str__(self):
        return self.title
    
    def save(self, obj, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_authenticated_user()
        self.updated_by = get_current_authenticated_user()
        super(CommonInfo, self).save(*args, **kwargs)

    def get_content_as_markdown(self):
        md = markdown.Markdown(
            extensions=['extra', 'admonition', 'sane_lists', 'toc'])
        return md.convert(self.content)

def file_upload_path(instance, filename):
    return f"{instance.upload_path}/{str(instance.info.pk)}/{str(instance.pk)}/{filename}"

class BaseAttachment(models.Model):
    objects = BaseManager()
    upload_path = ''
    info = models.ForeignKey(CommonInfo , on_delete=models.CASCADE)
    file = models.FileField(verbose_name='ファイル', upload_to=file_upload_path)
    filename = models.CharField(verbose_name='ファイル名', default="", null=True, blank=True, max_length=64)
    class Meta:
        abstract= True

    def save(self, *args, **kwargs):
        if self.id is None:
            upload_file = self.file
            self.filename = str(self.file)
            self.file = None
            super().save(*args, **kwargs)
            self.file = upload_file
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        else:
            if not os.path.isfile(f'f"uploads/info/{str(self.id)}/{str(self.info)}/abc.jpg"'):
                self.file_delete()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file_delete()
        super().delete(*args, **kwargs)

    def file_delete(self) -> None:
        if os.path.isdir(f'uploads/{self.upload_path}/{self.info.pk}/{self.id}'):
            shutil.rmtree(f'uploads/{self.upload_path}/{self.info.pk}/{self.id}')
