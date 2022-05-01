# Generated by Django 3.2 on 2022-05-01 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eqs', '0002_eqtype_slug'),
        ('infos', '0030_alter_info_eqtypes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='eqtypes',
            field=models.ManyToManyField(blank=True, to='eqs.Eqtype', verbose_name='装置型式'),
        ),
    ]
