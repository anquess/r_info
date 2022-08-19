from django.db import models

from rise_info.baseModels import CommonInfo, BaseAttachment, file_upload_path, BaseCommnets
from eqs.models import Eqtype

# Create your models here.


class TechSupports(CommonInfo):
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    inquiry = models.TextField(
        verbose_name='問い合わせ内容', default="", null=False, blank=True, max_length=2048)
    eqtypes = models.ManyToManyField(Eqtype, verbose_name='装置型式', blank=True)
    is_closed = models.BooleanField(verbose_name='解決済', default=False)

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
