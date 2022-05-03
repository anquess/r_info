# Generated by Django 3.2 on 2022-01-02 23:10

from django.db import migrations, models
import django.db.models.deletion
import rise_info.baseModels


class Migration(migrations.Migration):

    dependencies = [
        ('failuer_reports', '0012_auto_20220102_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=rise_info.baseModels.file_upload_path, verbose_name='ファイル')),
                ('filename', models.CharField(blank=True, default='', max_length=64, null=True, verbose_name='ファイル名')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='failuer_reports.failuerreport')),
            ],
            options={
                'db_table': 'failuer_report_attachments',
            },
        ),
        migrations.DeleteModel(
            name='FailRepoFile',
        ),
    ]
