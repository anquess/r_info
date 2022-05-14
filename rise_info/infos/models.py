from django.db import models

from rise_info.baseModels import CommonInfo, BaseAttachment, file_upload_path
from eqs.models import Eqtype

from datetime import date


class InfoTypeChoices(models.TextChoices):
    TECHINICAL = 'technical', '信頼性技術情報'
    FAILURE_CASE = 'failure_case', '障害事例情報'
    SAFETY = 'safety', '安全情報'
    EVENT = 'event', 'イベント情報'


class Info(CommonInfo):
    info_type = models.CharField(verbose_name='情報種別', max_length=16, choices=InfoTypeChoices.choices,
                                 default=InfoTypeChoices.TECHINICAL, null=False, blank=False)
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    managerID = models.CharField(
        verbose_name='管理番号', default="TMC-解析-", null=False, blank=False, max_length=32)
    sammary = models.TextField(
        verbose_name='概要', default="", null=False, blank=True, max_length=512)
    eqtypes = models.ManyToManyField(Eqtype, verbose_name='装置型式', blank=True)
    is_disclosed = models.BooleanField(verbose_name='公開可否', default=True)
    disclosure_date = models.DateField(
        verbose_name='公開日', default=date.today())

    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)

    class Meta:
        db_table = 'infos'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(Info, on_delete=models.CASCADE)
    upload_path = 'info'

    class Meta:
        db_table = 'info_attachment'
