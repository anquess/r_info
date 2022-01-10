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
from rise_info.baseModels import BaseManager

def isImportRow(row) -> bool:
    return dt.strptime(row['DATASAKUSEI_DATE'], '%Y/%m/%d %H:%M') > getLastUpdateAt('eqtype')

def eqtypes_csv_import():
    with open('uploads/documents/EQTypes.csv', 'rt', encoding = "utf-8-sig") as f:
        reader = csv.DictReader(f)
        eqtypes = [ row for row in reader ]
        eqtype_create_object=[]
        for row in eqtypes:
            sysupdtime = dt.strptime(row['DATASAKUSEI_DATE'], '%Y/%m/%d %H:%M')
            if isImportRow(row):
                if not Eqtype.objects.filter(id=row['SOCHIKATA']).exists():
                    eqtype_create_object.append(Eqtype(
                            id=row['SOCHIKATA'],
                            slug=slugify(row['SOCHIKATA']),
                            create_at=sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                    ))

        Eqtype.objects.bulk_create(eqtype_create_object)
        last_update_at = Eqtype.objects.all().aggregate(Max('create_at'))['create_at__max']
        setLastUpdateAt('eqtype', last_update_at.replace(tzinfo=pytz.timezone('Asia/Tokyo')))
        shutil.copy2('uploads/documents/EQTypes.csv','uploads/documents/EQTypes_tmp.csv')


class Eqtype(models.Model):
    objects = BaseManager()
    id = models.CharField(verbose_name='装置型式', primary_key=True, editable=False, max_length=24)
    slug = models.SlugField(verbose_name='装置型式(URL)', unique=True, null=False, editable=False, max_length=24)
    create_at = models.DateTimeField(verbose_name='登録日時')
    def __str__(self):
        return self.id
    def get_absolute_url(self):
        return reverse('eqtype_del', kwargs={'slug': self.slug})

    class Meta:
        db_table = 'eqtypes'
