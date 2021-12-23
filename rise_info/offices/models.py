from django.db import models
from django.urls import reverse
from rise_info.baseModels import BaseManager

from histories.models import HistoryDB
from accounts.models import createUser

import csv
import pytz
from datetime import datetime as dt


def offices_csv_import():
    history = HistoryDB.objects.get_or_none(slug='office')
    if history:
        last_update_at = history.update_at
    with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
        reader = csv.DictReader(f)
        offices = [ row for row in reader ]
    for row in offices:
        if (row['UNYOSTS_KBN'] == '0' and row['HOSHUINUMU_FLG'] == '1'and row['KANSHO_CD'] == row['JOCHUKANSHO_CD']):
            office = Office.objects.get_or_none(slug=row['KANSHO_CD'])
            if row['DATASHUSEI_DATE']:
                sysupdtime = dt.strptime(row['DATASHUSEI_DATE'], '%Y/%m/%d %H:%M:%S')
            else:
                sysupdtime = dt.strptime(row['SYSUPDTIME'], '%Y/%m/%d %H:%M:%S')
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
