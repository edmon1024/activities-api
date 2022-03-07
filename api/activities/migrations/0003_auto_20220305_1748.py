# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-03-05 23:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_auto_20220305_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('done', 'Done')], max_length=35, verbose_name='Status'),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled')], max_length=35, verbose_name='Status'),
        ),
    ]