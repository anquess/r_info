# Generated by Django 3.2 on 2021-12-28 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('failuer_reports', '0006_failuerreport_isrichtext'),
    ]

    operations = [
        migrations.RenameField(
            model_name='failuerreport',
            old_name='isRichText',
            new_name='is_rich_text',
        ),
    ]