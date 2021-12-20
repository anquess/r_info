import datetime
from django.db import models
from django.urls import reverse
from django.db.models import Max

import csv
from datetime import datetime as dt, tzinfo
import pytz


def offices_csv_import():
    with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
        reader = csv.DictReader(f)
        offices = [ row for row in reader ]
    for row in offices:
        if row['UNYOSTS_KBN'] != '2':
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
                Office.objects.create(
                    slug=row['KANSHO_CD'],
                    name=row['KANSHO_NM'],
                    shortcut_name=row['KANSHO_SNM'],
                    update_at=sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                )

class BaseManager(models.Manager):
    def get_or_none(self, **kwargs):
        """
        検索にヒットすればそのモデルを、しなければNoneを返します。
        """
        try:
            return self.get_queryset().get(**kwargs)
        except self.model.DoesNotExist:
            return None


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
