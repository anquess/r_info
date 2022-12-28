from django.db import models
from django.db.models import Max
from django.urls import reverse
from django.utils.text import slugify

import csv
import shutil
import pytz
from datetime import datetime as dt

from rise_info.baseModels import BaseManager
from histories.models import getLastUpdateAt, setLastUpdateAt


def isImportRow(row) -> bool:
    sysupdtime = dt.strptime(row['DATASAKUSEI_DATE'], '%Y/%m/%d %H:%M')
    sysupdtime = sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
    lastUpdateAt = getLastUpdateAt('eqtype').replace(
        tzinfo=pytz.timezone('Asia/Tokyo'))
    return sysupdtime > lastUpdateAt


def eqtypes_csv_import():
    with open('uploads/documents/EQTypes.csv', 'rt', encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        eqtypes = [row for row in reader]
        eqtype_create_object = []
        for row in eqtypes:
            sysupdtime = dt.strptime(row['DATASAKUSEI_DATE'], '%Y/%m/%d %H:%M')
            if isImportRow(row):
                if not Eqtype.objects.filter(id=row['SOCHIKATA']).exists():
                    eqtype_create_object.append(Eqtype(
                        id=row['SOCHIKATA'],
                        slug=slugify(row['SOCHIKATA']),
                        create_at=sysupdtime.replace(
                            tzinfo=pytz.timezone('Asia/Tokyo'))
                    ))

        Eqtype.objects.bulk_create(eqtype_create_object)
        last_update_at = Eqtype.objects.all().aggregate(
            Max('create_at'))['create_at__max']
        setLastUpdateAt('eqtype', last_update_at.replace(
            tzinfo=pytz.timezone('Asia/Tokyo')))
        shutil.copy2('uploads/documents/EQTypes.csv',
                     'uploads/documents/EQTypes_tmp.csv')


class DepartmentForEq(models.Model):
    objects = BaseManager()
    id = models.SlugField(verbose_name='担当部署略号',
                          primary_key=True, max_length=8)
    name = models.CharField(verbose_name="担当部署名", max_length=24)

    def __str__(self):
        return self.name


class EQ_class(models.Model):
    object = BaseManager()
    id = models.CharField(verbose_name='装置分類', max_length=16,
                          primary_key=True, editable=False)
    department = models.ManyToManyField(DepartmentForEq,
                                        verbose_name="装置担当部署", related_name="eq_class",
                                        null=True, blank=True)
    memo = models.TextField(
        verbose_name='備考', max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return self.id

    class Meta:
        db_table = 'eqclass'


class Eqtype(models.Model):
    objects = BaseManager()
    id = models.CharField(verbose_name='装置型式',
                          primary_key=True, editable=False, max_length=24)
    slug = models.SlugField(verbose_name='装置型式(URL)',
                            unique=True, null=False, editable=False,
                            max_length=24)
    eq_class = models.ForeignKey(
        EQ_class, verbose_name='装置分類', null=True, blank=True,
        related_name='eqtype', on_delete=models.CASCADE)
    create_at = models.DateTimeField(verbose_name='登録日時')

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse('eqtype_del', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'eqtypes'
