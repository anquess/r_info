from django.db import models
from django.urls import reverse
from django.db.models import Max

from rise_info.baseModels import BaseManager, csvFormatCheck, getSysupdtime
from histories.models import getLastUpdateAt, setLastUpdateAt
from accounts.models import createUser

import csv
import pytz
import shutil

def isImportRow(row) -> bool:
    return ( \
            row['UNYOSTS_KBN'] == '0' \
            and row['HOSHUINUMU_FLG'] == '1' \
            and row['KANSHO_CD'] == row['JOCHUKANSHO_CD']  \
            and getSysupdtime(row) > getLastUpdateAt('office') \
        )

def formatCheck(offices) -> bool:
    return csvFormatCheck(
        offices, (
            'KANSHO_CD',
            'KANSHO_NM',
            'KANSHO_SNM',
            'DATASHUSEI_DATE',
            'SYSUPDTIME',
            )
        )

def offices_csv_import():
    with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
        reader = csv.DictReader(f)
        offices = [ row for row in reader ]
    if formatCheck(offices[0]):
        for row in offices:
            sysupdtime = getSysupdtime(row)
            if isImportRow(row):
                office = Office.objects.get_or_none(slug=row['KANSHO_CD'])
                if office:
                    if sysupdtime > office.update_at.replace(tzinfo=None):
                        office.name=row['KANSHO_NM']
                        office.shortcut_name=row['KANSHO_SNM']
                        office.update_at=sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                        office.save()
                else:
                    office = Office.objects.create(
                        slug=row['KANSHO_CD'],
                        name=row['KANSHO_NM'],
                        shortcut_name=row['KANSHO_SNM'],
                        update_at=sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                    )
                    createUser(office)
        last_update_at = Office.objects.all().aggregate(Max('update_at'))['update_at__max']
        setLastUpdateAt('office', last_update_at.replace(tzinfo=pytz.timezone('Asia/Tokyo')))
        shutil.copy2('uploads/documents/Offices.csv','uploads/documents/Offices_tmp.csv')

class Office(models.Model):
    objects = BaseManager()
    slug = models.SlugField(verbose_name='官署コード', unique=True,null=False, blank=False, max_length=4)
    name = models.CharField(verbose_name='官署名',null=False, blank=False, max_length=32)
    shortcut_name = models.CharField(verbose_name='官署略称',null=False, blank=False, max_length=8)
    update_at = models.DateTimeField(verbose_name='更新日時')

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('office_detail', kwargs={'slug': self.slug})
    
    class Meta:
        db_table = 'offices'
