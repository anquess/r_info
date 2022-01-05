from django.db import models

from rise_info.baseModels import BaseManager, CommonInfo, BaseAttachment, file_upload_path

class FailuerReport(CommonInfo):
    sammary = models.TextField(verbose_name='概要', default="", null=False, blank=True, max_length=512)
    is_operatinal_impact = models.BooleanField(verbose_name='運用への影響有無', default=False)
    operatinal_impact = models.CharField(verbose_name='運用への影響', default="", null=False, blank=True, max_length=128)
    is_flight_impact = models.BooleanField(verbose_name='運航への影響有無', default=False)
    flight_impact = models.CharField(verbose_name='運航への影響', default="", null=False, blank=True, max_length=128)

    def save(self, *args, **kwargs):
        super(FailuerReport, self).save(self, *args, **kwargs)
    
    class Meta:
        db_table = 'failuer_reports'

class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(FailuerReport , on_delete=models.CASCADE)
    upload_path = 'fail_rep'
    class Meta:
        db_table = 'failuer_report_attachments'

class Circumstances(models.Model):
    object = BaseManager()
    info = models.ForeignKey(FailuerReport , on_delete=models.CASCADE)
    date = models.DateField(verbose_name='日付', null=True, blank=True)
    time = models.TimeField(verbose_name='時間', null=True, blank=True)
    event = models.TextField(verbose_name='事案', max_length=256)
