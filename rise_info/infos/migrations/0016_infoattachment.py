# Generated by Django 3.2 on 2022-01-01 05:45

from django.db import migrations, models
import django.db.models.deletion
import infos.models


class Migration(migrations.Migration):

    dependencies = [
        ('infos', '0015_delete_infoattachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, default='', max_length=64, upload_to=infos.models.file_upload_path, verbose_name='ファイル名')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='infos.info')),
            ],
            options={
                'db_table': 'info_attachments',
            },
        ),
    ]
