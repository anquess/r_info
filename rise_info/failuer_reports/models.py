from django.db import models
from django_currentuser.db.models import CurrentUserField

from addresses.models import Addresses
from eqs.models import DepartmentForEq
from rise_info.baseModels import CommonInfo, BaseAttachment


class ConfirmationTypeChoices(models.TextChoices):
    UNNECESSASY = 'unnecessary', '確認不要'
    CONFIRMED = 'confirmed', '確認済'
    CHECKING_NOW = 'checking_now', '確認中'


class IsConfirmChoices(models.TextChoices):
    NONE = 'none', '無'
    YES = 'yes', '有'
    CHECKING_NOW = 'checking_now', '確認中'


class RegisterStatusChoices(models.TextChoices):
    TEMP = 'temporaty', '一時保存'
    SENDED = 'sended', '送信済み'


class FailuerReport(CommonInfo):
    failuer_date = models.DateField(
        verbose_name='障害発生日', null=True, blank=True,
        help_text="必須"
    )
    failuer_time = models.TimeField(
        verbose_name='障害発生時', null=True, blank=True,
        help_text="必須"
    )
    date_time_confirmation = models.CharField(
        verbose_name='日時確認状態',
        max_length=16,
        choices=ConfirmationTypeChoices.choices,
        help_text='運用者等の管技官以外からの障害検知した場合は当該者と障害発生日時の調整が必要',
        default=ConfirmationTypeChoices.CHECKING_NOW, null=False, blank=False
    )
    failuer_place = models.CharField(
        verbose_name='障害発生場所', default="xx空港",
        null=False, blank=True, max_length=128,
        help_text="必須"
    )
    eq = models.CharField(
        verbose_name="障害装置", null=False,
        blank=True, max_length=128,
        help_text="必須"
    )
    department = models.ManyToManyField(
        DepartmentForEq, verbose_name='関係装置分類', blank=True,
        help_text='関係官署と関係装置分類から配信先を自動判定(必須)',
    )
    sammary = models.TextField(
        verbose_name='障害概要', default="確認中", null=False, blank=True,
        max_length=1024, help_text="必須項目\n何がどうなったか簡潔に\n例:LOC が●●ALM発生により停止"
    )
    cause = models.TextField(
        verbose_name='障害原因', default="確認中", null=False, blank=True,
        max_length=1024, help_text="必須項目\n現時点で判明している事柄を記載\n例:詳細確認中"
    )
    recovery_date = models.DateField(
        verbose_name='復旧日', null=True, blank=True,
        help_text="復旧日　復旧後記載"
    )
    recovery_time = models.TimeField(
        verbose_name='復旧時', null=True, blank=True,
        help_text="復旧時間　復旧後記載"
    )
    recovery_propects = models.TextField(
        verbose_name='復旧の見通し', default="確認中",
        null=False, blank=True, max_length=1024,
        help_text="必須項目\n分かる範囲で予定等を記載\n例:保守員の派遣を調整中"
    )
    is_flight_impact = models.CharField(
        verbose_name='運航への影響有無', max_length=16,
        choices=IsConfirmChoices.choices,
        default=IsConfirmChoices.CHECKING_NOW,
        null=False, blank=False
    )
    flight_impact = models.CharField(
        verbose_name='運航への影響', default="",
        null=False, blank=True, max_length=128
    )
    notam = models.CharField(
        verbose_name="ノータム",
        null=False, blank=True, max_length=512,
        help_text="ノータム発行があれば記載"
    )
    is_press = models.CharField(
        verbose_name='取材の有無', max_length=16, choices=IsConfirmChoices.choices,
        default=IsConfirmChoices.CHECKING_NOW, null=False, blank=False
    )
    press_contents = models.TextField(
        verbose_name='取材内容', default="取材の内容",
        null=False, blank=True, max_length=1024,
        help_text="\
有の場合はその概要を記入\n\
基本対応\n\
    ①基本的に発生事案については、全ての事項を本省管制技術課で対応\n\
    ②官署への取材等がおこなれる場合を想定し、関係官署の広報担当者に\n\
    　答弁ラインを連絡するとともに、当該官署における航法対応の体制\n\
    　について確認を行う(答弁は当該官署の広報担当者にて実施)\n\
    ③現地官署での取材内容は、本省管制技術課危機管理担当に逐次報告"
    )
    content = models.TextField(
        verbose_name='備考', default="", null=False, blank=True, max_length=4096
    )
    select_register = models.CharField(
        verbose_name='登録状態', max_length=16,
        choices=RegisterStatusChoices.choices,
        default=RegisterStatusChoices.TEMP, null=False, blank=False
    )

    def save(self, *args, **kwargs):
        if 'temp_info' in kwargs:
            self.title = kwargs['temp_info'].title
            self.content = kwargs['temp_info'].content
            self.created_by = kwargs['temp_info'].created_by
            self.created_at = kwargs['temp_info'].created_at
            self.updated_at = kwargs['temp_info'].updated_at
            self.updated_by = kwargs['temp_info'].updated_by
            self.failuer_date = kwargs['temp_info'].failuer_date
            self.failuer_time = kwargs['temp_info'].failuer_time
            self.date_time_confirmation = kwargs['temp_info'].date_time_confirmation
            self.failuer_place = kwargs['temp_info'].failuer_place
            self.eq = kwargs['temp_info'].eq
            self.sammary = kwargs['temp_info'].sammary
            self.recovery_date = kwargs['temp_info'].recovery_date
            self.recovery_time = kwargs['temp_info'].recovery_time
            self.recovery_propects = kwargs['temp_info'].recovery_propects
            self.is_flight_impact = kwargs['temp_info'].is_flight_impact
            self.flight_impact = kwargs['temp_info'].flight_impact
            self.is_press = kwargs['temp_info'].is_press
            self.press_contents = kwargs['temp_info'].press_contents
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


class FailuerReportRelation(FailuerReport):
    send_repo = models.OneToOneField(
        FailuerReport, on_delete=models.DO_NOTHING,
        related_name='sended', verbose_name='送信ログ', null=True, blank=True
    )
    dest_list = models.ManyToManyField(
        Addresses, related_name='failuer_repo_list', null=True, blank=True
    )

    class Meta:
        db_table = 'failuer_repo_list'
