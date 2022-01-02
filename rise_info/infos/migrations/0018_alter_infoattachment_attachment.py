# Generated by Django 3.2 on 2022-01-01 06:19

from django.db import migrations, models
import infos.models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0017_alter_infoattachment_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infoattachment',
            name='attachment',
            field=models.FileField(default='Asia/Tokyo', upload_to=infos.models.file_upload_path, verbose_name='ファイル名'),
            preserve_default=False,
        ),
    ]