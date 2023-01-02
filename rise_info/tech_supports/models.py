from django.db import models

from eqs.models import Eqtype
from rise_info.baseModels import CommonInfo, BaseAttachment, file_upload_path, BaseCommnets
from rise_info.choices import RegisterStatusChoicesSupo, InfoTypeChoicesSupo
# Create your models here.


class TechSupports(CommonInfo):
    info_type = models.CharField(
        verbose_name='情報種別', max_length=16, choices=InfoTypeChoicesSupo.choices,
        default=InfoTypeChoicesSupo.SUPPORT, null=False, blank=False)
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    inquiry = models.TextField(
        verbose_name='問い合わせ内容', default="", null=False, blank=True, max_length=2048)
    eqtypes = models.ManyToManyField(Eqtype, verbose_name='装置型式', blank=True)
    select_register = models.CharField(
        verbose_name='登録状態', max_length=16,
        choices=RegisterStatusChoicesSupo.choices,
        default=RegisterStatusChoicesSupo.NOT_REGISTERED, null=False, blank=False
    )

    def save(self, *args, **kwargs):
        super(TechSupports, self).save(self, *args, **kwargs)

    def delete(self, *args, **kwargs):
        for attachment in self.attachmentfile_set.all():
            attachment.delete()
        return super().delete(*args, **kwargs)

    class Meta:
        db_table = 'tech_supports'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(
        TechSupports, on_delete=models.CASCADE)
    upload_path = 'tech_support'

    class Meta:
        db_table = 'tech_support_attachment'


class TechSupportComments(BaseCommnets):
    info = models.ForeignKey(
        TechSupports, related_name='techSupportComment', on_delete=models.CASCADE)
    upload_path = 'tech_support_comments'

    class Meta:
        db_table = 'tech_support_comments'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.info.save()
        super(TechSupportComments, self).save(*args, **kwargs)
