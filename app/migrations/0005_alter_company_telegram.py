# Generated by Django 3.2.4 on 2021-06-09 19:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('app', '0004_alter_company_telegram'), ]

    operations = [migrations.AlterField(model_name='company', name='telegram',
        field=models.CharField(blank=True, help_text='Company Telegram contact', max_length=30), ), ]