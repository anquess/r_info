# Generated by Django 3.2 on 2022-04-12 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eqs', '0002_eqtype_slug'),
        ('infos', '0025_auto_20220103_1508'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='eqtypes',
            field=models.ManyToManyField(to='eqs.Eqtype'),
        ),
    ]
