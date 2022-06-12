from django.db import models

from rise_info.baseModels import CommonInfo, BaseAttachment, file_upload_path
from eqs.models import Eqtype
from offices.models import Office

from datetime import date

from openpyxl import load_workbook


def importInfo():
    infotype = [
        InfoTypeChoices.TECHINICAL,
        InfoTypeChoices.FAILURE_CASE,
        InfoTypeChoices.SAFETY,
        InfoTypeChoices.EVENT,
    ]
    wb_info = load_workbook('test_data/info.xlsx')
    ws_info = wb_info['info']
    infos = []
    Info.objects.all().delete()
    for row in ws_info.iter_rows(min_row=2):
        if row[5].value < 5:
            if row[3].value:
                id = row[0].value
                managerID = row[1].value
                title = row[2].value
                sammary = row[3].value[0:511]
                content = row[3].value
                disclosure_date = row[6].value
                is_disclosed = row[8].value
                info_type = infotype[row[5].value - 1]

                info = Info(id=id, managerID=managerID, title=title, sammary=sammary, content=content,
                            disclosure_date=disclosure_date, info_type=info_type, is_disclosed=is_disclosed)
                infos.append(info)
    Info.objects.bulk_create(infos)
    importInfoEqTypes()


def importInfoEqTypes():
    wb_info_eqtype = load_workbook('test_data/infoEqType.xlsx')
    ws_info_eq_type = wb_info_eqtype['infoEqType']

    infos = []
    info_eq_type = {}
    info_id = None
    eq_types = []
    for row in ws_info_eq_type.iter_rows(min_row=2):
        if info_id == row[1].value:
            eq_type = Eqtype.objects.get_or_none(
                id=row[2].value + '_' + row[3].value)
            if eq_type:
                eq_types.append(eq_type)
        else:
            if info_id:
                info_eq_type[info_id] = eq_types

            info_id = row[1].value
            eq_types = []

    info_eq_type[info_id] = eq_types
    for key, val in info_eq_type.items():
        print(key)
        if Info.objects.filter(id=int(key)).exists():
            info = Info.objects.get_or_create(id=key)
            print(info, val)
            for eq in val:
                info[0].eqtypes.add(eq)
            infos.append(info[0])


class InfoTypeChoices(models.TextChoices):
    TECHINICAL = 'technical', '信頼性技術情報'
    FAILURE_CASE = 'failure_case', '障害事例情報'
    SAFETY = 'safety', '安全情報'
    EVENT = 'event', 'イベント情報'
    MANUAL = 'manual', '完成図書差し替え'


class Info(CommonInfo):
    info_type = models.CharField(verbose_name='情報種別', max_length=16, choices=InfoTypeChoices.choices,
                                 default=InfoTypeChoices.TECHINICAL, null=False, blank=False)
    is_rich_text = models.BooleanField(
        verbose_name='リッチテキスト有効', default=False, help_text='内容のリッチテキスト有効/無効')
    managerID = models.CharField(
        verbose_name='管理番号', default="TMC-解析-", null=False, blank=False, max_length=32)
    sammary = models.TextField(
        verbose_name='概要', default="", null=False, blank=True, max_length=512)
    is_add_eqtypes = models.BooleanField(verbose_name='装置型式特定', default=True)
    eqtypes = models.ManyToManyField(Eqtype, verbose_name='装置型式', blank=True)
    is_add_offices = models.BooleanField(verbose_name='官署特定', default=True)
    offices = models.ManyToManyField(Office, verbose_name='官署', blank=True)
    is_disclosed = models.BooleanField(verbose_name='公開', default=True)
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
