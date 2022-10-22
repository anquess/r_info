from django.db import models

from rise_info.baseModels import CommonInfo, BaseAttachment


class ConfirmationTypeChoices(models.TextChoices):
    UNNECESSASY = 'unnecessary', '確認不要'
    CONFIRMED = 'confirmed', '確認済'
    CHECKING_NOW = 'checking_now', '確認中'


class FailuerReport(CommonInfo):
    failuer_date = models.DateField(
        verbose_name='障害発生日', null=True, blank=True)
    failuer_time = models.TimeField(
        verbose_name='障害発生時', null=True, blank=True)
    date_time_confirmation = models.CharField(verbose_name='日時確認状態', max_length=16, choices=ConfirmationTypeChoices.choices,
                                              help_text='運用者等の管技官以外からの障害検知した場合は当該者と障害発生日時の調整が必要',
                                              default=ConfirmationTypeChoices.CHECKING_NOW, null=False, blank=False)
    sammary = models.TextField(
        verbose_name='障害状況', default="確認中", null=False, blank=True, max_length=512)
    is_operatinal_impact = models.BooleanField(
        verbose_name='運用への影響有無', default=False)
    operatinal_impact = models.CharField(
        verbose_name='運用への影響', default="", null=False, blank=True, max_length=128)
    is_flight_impact = models.BooleanField(
        verbose_name='運航への影響有無', default=False)
    flight_impact = models.CharField(
        verbose_name='運航への影響', default="", null=False, blank=True, max_length=128)

    def save(self, *args, **kwargs):
        super(FailuerReport, self).save(self, *args, **kwargs)

    class Meta:
        db_table = 'failuer_reports'


class AttachmentFile(BaseAttachment):
    info = models.ForeignKey(FailuerReport, on_delete=models.CASCADE)
    upload_path = 'fail_rep'

    class Meta:
        db_table = 'failuer_report_attachments'


class Circumstances(models.Model):
    info = models.ForeignKey(FailuerReport, on_delete=models.CASCADE)
    date = models.DateField(verbose_name='日付', null=True, blank=True)
    time = models.TimeField(verbose_name='時間', null=True, blank=True)
    event = models.TextField(verbose_name='事案', max_length=256)

    class Meta:
        db_table = 'circumstance'
