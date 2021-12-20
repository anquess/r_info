from django.db import models
from django.urls import reverse

import csv

class Office(models.Model):
    slug = models.SlugField(verbose_name='官署コード', unique=True,null=False, blank=False, max_length=4)
    name = models.CharField(verbose_name='官署名',null=False, blank=False, max_length=32)
    shortcut_name = models.CharField(verbose_name='官署略称',null=False, blank=False, max_length=8)
    update_at = models.DateTimeField(verbose_name='更新日時')

    def __str__(self):
        return self.slug
    
    def get_absolute_url(self):
        return reverse('office_detail', kwargs={'slug': self.slug})
    
    def csv_import(self):
        with open('uploads/documents/Offices.csv', 'rt', encoding='cp932') as f:
            reader = csv.reader(f)
            offices = [ row for row in reader ]
        for row in offices:
            print(row[0])

    class Meta:
        db_table = 'offices'
