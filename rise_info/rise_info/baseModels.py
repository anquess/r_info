from django.db import models
from django_currentuser.db.models import CurrentUserField
from django_currentuser.middleware import (get_current_authenticated_user)

from .choices import RegisterStatusChoices

from datetime import datetime as dt
import os
import shutil
import markdown
import pytz


def getSysupdtime(row) -> dt:
    if row['DATASHUSEI_DATE']:
        str_sysupdtime = row['DATASHUSEI_DATE']
    elif row['SYSUPDTIME']:
        str_sysupdtime = row['SYSUPDTIME']
    else:
        str_sysupdtime = row['DATASAKUSEI_DATE']
    if str_sysupdtime.count(':') == 1:
        sysupdtime = dt.strptime(str_sysupdtime, '%Y/%m/%d %H:%M')
    else:
        sysupdtime = dt.strptime(str_sysupdtime, '%Y/%m/%d %H:%M:%S')
    sysupdtime = sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
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
    title = models.CharField(
        verbose_name='タイトル', default="", null=False, blank=False, max_length=128)
    content = models.TextField(
        verbose_name='内容', default="", null=False, blank=True, max_length=4096)
    select_register = models.CharField(
        verbose_name='登録状態', max_length=16,
        choices=RegisterStatusChoices.choices,
        default=RegisterStatusChoices.TEMP, null=False, blank=False
    )
    created_by = CurrentUserField(verbose_name='登録者', on_update=True,
                                  related_name='%(app_label)s_%(class)s_create', null=False, blank=False)
    created_at = models.DateTimeField(
        verbose_name='投稿日', auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(
        verbose_name='更新日', auto_now=True, null=False, blank=False)
    updated_by = CurrentUserField(verbose_name='更新者', on_update=True,
                                  related_name='%(app_label)s_%(class)s_update', null=False, blank=False)

    class Meta:
        abstract = True

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
    if hasattr(instance, 'info'):
        info_pk = instance.info.pk
    else:
        info_pk = instance.content.pk

    return f"{instance.upload_path}/{str(info_pk)}/{str(instance.pk)}/{filename}"


class BaseAttachment(models.Model):
    objects = BaseManager()
    upload_path = ''
    info = models.ForeignKey(CommonInfo, on_delete=models.CASCADE)
    file = models.FileField(verbose_name='ファイル', upload_to=file_upload_path)
    filename = models.CharField(
        verbose_name='ファイル名', default="", null=True, blank=True, max_length=64)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.id is None:
            upload_file = self.file
            self.filename = str(self.file)
            self.file = None
            super().save(*args, **kwargs)
            self.file = upload_file
            if "force_insert" in kwargs:
                kwargs.pop("force_insert")
        elif not os.path.isfile(f'uploads/{str(self.file)}'):
            self.file_delete()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file_delete()
        super().delete(*args, **kwargs)

    def file_delete(self) -> None:
        if os.path.isdir(f'uploads/{self.upload_path}/{self.info.pk}/{self.id}'):
            shutil.rmtree(
                f'uploads/{self.upload_path}/{self.info.pk}/{self.id}')


class BaseCommnets(models.Model):
    objects = BaseManager()
    upload_path = ''
    comment_txt = models.TextField(
        verbose_name='コメント', default="", null=False, blank=True, max_length=512)
    file = models.FileField(
        verbose_name='ファイル', upload_to=file_upload_path)
    filename = models.CharField(
        verbose_name='ファイル名', default="", null=True, blank=True, max_length=64)
    created_by = CurrentUserField(verbose_name='登録者', on_update=True,
                                  related_name='%(app_label)s_%(class)s_create', null=False, blank=False)
    created_at = models.DateTimeField(
        verbose_name='投稿日', auto_now_add=True, null=False, blank=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created_by = get_current_authenticated_user()
        upload_file = self.file
        self.filename = str(self.file)
        self.file = None
        super().save(*args, **kwargs)
        self.file = upload_file
        if "force_insert" in kwargs:
            kwargs.pop("force_insert")

        super(BaseCommnets, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file_delete()
        super().delete(*args, **kwargs)

    def file_delete(self) -> None:
        if hasattr(self, 'info'):
            info_pk = self.info.pk
        else:
            info_pk = self.content.pk
        if os.path.isdir(f'uploads/{self.upload_path}/{info_pk}/{self.id}'):
            shutil.rmtree(
                f'uploads/{self.upload_path}/{info_pk}/{self.id}')
