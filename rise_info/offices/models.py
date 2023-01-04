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

bigAlphaNumeric = RegexValidator(
    r'^[0-9A-Z]*$', 'Only A-Z and 0-9 chatacters are allowed')


def isImportRow(row) -> bool:
    sysupdtime = getSysupdtime(row)
    lastupdtime = getLastUpdateAt('office')
    try:
        if str(sysupdtime.tzinfo) == 'UTC':
            raise ValueError('sysupdtime is ' + str(sysupdtime.tzinfo))
        if str(lastupdtime.tzinfo) == 'UTC':
            raise ValueError('lastupdtime is ' + str(lastupdtime.tzinfo))
    except ValueError as e:
        print(e)
    return (
        row['UNYOSTS_KBN'] == '0'
        and row['HOSHUINUMU_FLG'] == '1'
        and row['KANSHO_CD'] == row['JOCHUKANSHO_CD']
        and sysupdtime > lastupdtime
    )


def offices_csv_import():
    with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
        reader = csv.DictReader(f)
        offices = [row for row in reader]
        office_create_object = []
        office_update_object = []
        user_object = []
        for row in offices:
            sysupdtime = getSysupdtime(row)
            if isImportRow(row):
                if Office.objects.filter(id=row['KANSHO_CD']).exists():
                    office = Office.objects.get(id=row['KANSHO_CD'])
                    if sysupdtime > office.update_at.replace(tzinfo=pytz.timezone('Asia/Tokyo')):
                        office.name = row['KANSHO_NM']
                        office.unyo_sts = (row['UNYOSTS_KBN'] == '0')
                        office.shortcut_name = row['KANSHO_SNM']
                        office.update_at = sysupdtime.replace(
                            tzinfo=pytz.timezone('Asia/Tokyo'))
                        office_update_object.append(office)
                        user_object.append({
                            'username': row['KANSHO_CD'],
                            'is_active': (row['UNYOSTS_KBN'] == '0'),
                            'first_name': row['KANSHO_NM'],
                            'last_name': row['KANSHO_SNM'],
                        })
                else:
                    office_create_object.append(Office(
                        id=row['KANSHO_CD'],
                        unyo_sts=(row['UNYOSTS_KBN'] == '0'),
                        name=row['KANSHO_NM'],
                        shortcut_name=row['KANSHO_SNM'],
                        update_at=sysupdtime.replace(
                            tzinfo=pytz.timezone('Asia/Tokyo'))
                    ))
                    user_object.append({
                        'username': row['KANSHO_CD'],
                        'is_active': (row['UNYOSTS_KBN'] == '0'),
                        'first_name': row['KANSHO_NM'],
                        'last_name': row['KANSHO_SNM'],
                    })

        Office.objects.bulk_create(office_create_object)
        Office.objects.bulk_update(office_update_object, fields=[
                                   'name', 'shortcut_name', 'update_at', ])
        createUser(user_object)
        last_update_at = Office.objects.all().aggregate(
            Max('update_at'))['update_at__max']
        setLastUpdateAt('office', last_update_at.replace(
            tzinfo=pytz.timezone('Asia/Tokyo')))
        shutil.copy2('uploads/documents/Offices.csv',
                     'uploads/documents/Offices_tmp.csv')


class OfficesGroup(models.Model):
    objects = BaseManager()
    group_name = models.CharField(
        verbose_name='グループ名', null=False, blank=False, max_length=32)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = 'offices_groups'


class Office(models.Model):
    objects = BaseManager()
    id = models.SlugField(verbose_name='官署コード', primary_key=True,
                          editable=False, validators=[bigAlphaNumeric],
                          max_length=4)
    unyo_sts = models.BooleanField(verbose_name='運用状態', default=True)
    name = models.CharField(
        verbose_name='官署名', null=False, blank=False, max_length=32)
    shortcut_name = models.CharField(
        verbose_name='官署略称', null=False, blank=False, max_length=8)
    offices_group = models.ManyToManyField(
        OfficesGroup, verbose_name='所属官署グループ', related_name='Offices')
    update_at = models.DateTimeField(verbose_name='更新日時')

    def __str__(self):
        return self.shortcut_name

    def get_absolute_url(self):
        return reverse('office_detail', kwargs={'id': self.id})

    class Meta:
        db_table = 'offices'
