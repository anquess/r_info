from django.db import models

from addresses.models import Addresses
from eqs.models import Eqtype
from rise_info.baseModels import CommonInfo, BaseAttachment, BaseCommnets
from rise_info.choices import RegisterStatusChoices, InfoTypeChoicesSupo


class TechSupports(CommonInfo):
    info_type = models.CharField(
        verbose_name='情報種別', max_length=16,
        choices=InfoTypeChoicesSupo.choices,
        default=InfoTypeChoicesSupo.SUPPORT,
        null=False, blank=False)
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False,
        help_text='内容のリッチテキスト有効/無効')
    inquiry = models.TextField(
        verbose_name='問い合わせ内容', default="", null=False, blank=True,
        max_length=2048)
    eqtypes = models.ManyToManyField(
        Eqtype, verbose_name='装置型式', null=True, blank=True,
        related_name='tech_supo')
    addresses = models.ManyToManyField(
        Addresses, verbose_name='受信アドレス', null=True, blank=True,
        related_name='tech_support')

    def save(self, *args, **kwargs):
        super(TechSupports, self).save(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        for attachment in self.attachmentfile_set.all():
            attachment.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = 'tech_supports'
        verbose_name = '官署発信(全データ)'
        verbose_name_plural = '官署発信一覧(全データ)'

class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(
        TechSupports, on_delete=models.CASCADE)
    upload_path = 'tech_support'

    class Meta:
        db_table = 'tech_support_attachment'
        verbose_name = '官署発信添付ファイル'
        verbose_name_plural = '官署発信添付ファイル一覧'


class TechSupportComments(BaseCommnets):
    info = models.ForeignKey(
        TechSupports, related_name='techSupportComment',
        on_delete=models.CASCADE)
    upload_path = 'tech_support_comments'

    class Meta:
        db_table = 'tech_support_comments'
        verbose_name = '官署発信コメント'
        verbose_name_plural = '官署発信コメント一覧'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.info.save()
        super(TechSupportComments, self).save(*args, **kwargs)


class TechSupportsRelation(TechSupports):
    send_info = models.OneToOneField(
        TechSupports, on_delete=models.DO_NOTHING, related_name='sended',
        verbose_name='送信ログ', null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.send_info:
            self.send_info.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = 'techSupport_list'
        verbose_name = '官署発信(一時保存)'
        verbose_name_plural = '官署発信一覧(一時保存)'
