# Generated by Django 3.2 on 2022-01-01 07:21

from django.db import migrations, models
import django.db.models.deletion
import rise_info.baseModels


class Migration(migrations.Migration):

    dependencies = [
        ('failuer_reports', '0007_rename_isrichtext_failuerreport_is_rich_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailuerReportAttachmentFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(upload_to=rise_info.baseModels.file_upload_path, verbose_name='ファイル名')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='failuer_reports.failuerreport')),
            ],
            options={
                'db_table': 'fail_report_attachments',
            },
        ),
    ]
