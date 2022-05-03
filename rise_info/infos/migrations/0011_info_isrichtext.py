# Generated by Django 3.2 on 2021-12-28 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0010_alter_info_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='isRichText',
            field=models.BooleanField(default=False, help_text='内容のリッチテキスト有効/無効', verbose_name='リッチテキスト有効'),
        ),
    ]
