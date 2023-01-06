from django.db import models

from addresses.models import Addresses
from eqs.models import Eqtype
from offices.models import Office
from rise_info.baseModels import CommonInfo, BaseAttachment, BaseCommnets
from rise_info.choices import InfoTypeChoices

from datetime import date


class Info(CommonInfo):
    info_type = models.CharField(
        verbose_name='情報種別', max_length=16, choices=InfoTypeChoices.choices,
        default=InfoTypeChoices.TECHINICAL, null=False, blank=False)
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    managerID = models.CharField(
        verbose_name='管理番号', default="TMC-解析-",
        null=False, blank=False, max_length=32)
    sammary = models.TextField(
        verbose_name='概要', default="", null=False, blank=True, max_length=512)
    is_add_eqtypes = models.BooleanField(verbose_name='装置型式特定', default=True)
    eqtypes = models.ManyToManyField(Eqtype, verbose_name='装置型式', blank=True)
    is_add_offices = models.BooleanField(verbose_name='官署特定', default=True)
    offices = models.ManyToManyField(Office, verbose_name='官署', blank=True)
    disclosure_date = models.DateField(
        verbose_name='公開日', default=date.today())
    addresses = models.ManyToManyField(
        Addresses, verbose_name='受信アドレス', null=True, blank=True,
        related_name='infos')

    def save(self, *args, **kwargs):
        super(Info, self).save(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        for attachment in self.attachmentfile_set.all():
            attachment.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = 'infos'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(
        Info, on_delete=models.CASCADE)
    upload_path = 'info'

    class Meta:
        db_table = 'info_attachment'


class InfoComments(BaseCommnets):
    info = models.ForeignKey(
        Info, related_name='infoComment', on_delete=models.CASCADE)
    upload_path = 'info_comments'

    class Meta:
        db_table = 'info_comments'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.info.save()
        super(InfoComments, self).save(*args, **kwargs)


class InfoRelation(Info):
    send_info = models.OneToOneField(
        Info, on_delete=models.DO_NOTHING, related_name='sended',
        verbose_name='送信ログ', null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.send_info:
            self.send_info.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = 'info_list'
