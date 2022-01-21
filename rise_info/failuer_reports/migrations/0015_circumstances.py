# Generated by Django 3.2 on 2022-01-05 08:11

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('failuer_reports', '0014_remove_failuerreport_is_rich_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Circumstances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True, verbose_name='日付')),
                ('time', models.TimeField(blank=True, null=True, verbose_name='時間')),
                ('info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='failuer_reports.failuerreport')),
            ],
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]