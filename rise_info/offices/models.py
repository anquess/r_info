from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Max
from django.urls import reverse

from rise_info.baseModels import BaseManager, getSysupdtime
from histories.models import getLastUpdateAt, setLastUpdateAt
from accounts.models import createUser

import csv
import pytz
import shutil

bigAlphaNumeric = RegexValidator(r'^[0-9A-Z]*$', 'Only A-Z and 0-9 chatacters are allowed')

def isImportRow(row) -> bool:
    return ( \
            row['UNYOSTS_KBN'] == '0' \
            and row['HOSHUINUMU_FLG'] == '1' \
            and row['KANSHO_CD'] == row['JOCHUKANSHO_CD']  \
            and getSysupdtime(row) > getLastUpdateAt('office') \
        )

def offices_csv_import():
    with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
        reader = csv.DictReader(f)
        offices = [ row for row in reader ]
        office_create_object=[]
        office_update_object=[]
        user_object=[]
        for row in offices:
            sysupdtime = getSysupdtime(row)
            if isImportRow(row):
                if Office.objects.filter(id=row['KANSHO_CD']).exists():
                    office = Office.objects.get(id=row['KANSHO_CD'])
                    if sysupdtime > office.update_at.replace(tzinfo=None):
                        office.name=row['KANSHO_NM']
                        office.shortcut_name=row['KANSHO_SNM']
                        office.update_at=sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                        office_update_object.append(office)
                        user_object.append({
                            'username':row['KANSHO_CD'],
                            'first_name':row['KANSHO_NM'],
                            'last_name':row['KANSHO_SNM'],
                            })
                else:
                    office_create_object.append(Office(
                            id=row['KANSHO_CD'],
                            name=row['KANSHO_NM'],
                            shortcut_name=row['KANSHO_SNM'],
                            update_at=sysupdtime.replace(tzinfo=pytz.timezone('Asia/Tokyo'))
                    ))
                    user_object.append({
                            'username':row['KANSHO_CD'],
                            'first_name':row['KANSHO_NM'],
                            'last_name':row['KANSHO_SNM'],
                            })

        Office.objects.bulk_create(office_create_object)
        Office.objects.bulk_update(office_update_object, fields=['name', 'shortcut_name', 'update_at',])
        createUser(user_object)
        last_update_at = Office.objects.all().aggregate(Max('update_at'))['update_at__max']
        setLastUpdateAt('office', last_update_at.replace(tzinfo=pytz.timezone('Asia/Tokyo')))
        shutil.copy2('uploads/documents/Offices.csv','uploads/documents/Offices_tmp.csv')

class Office(models.Model):
    objects = BaseManager()
    id = models.SlugField(verbose_name='官署コード', primary_key=True, editable=False, validators=[bigAlphaNumeric], max_length=4)
    name = models.CharField(verbose_name='官署名',null=False, blank=False, max_length=32)
    shortcut_name = models.CharField(verbose_name='官署略称',null=False, blank=False, max_length=8)
    update_at = models.DateTimeField(verbose_name='更新日時')

    def __str__(self):
        return self.id
    
    def get_absolute_url(self):
        return reverse('office_detail', kwargs={'id': self.id})
    
    class Meta:
        db_table = 'offices'
