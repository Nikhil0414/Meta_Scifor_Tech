# Generated by Django 4.2.7 on 2024-02-05 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userModule', '0005_orderstbl_tracking_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderstbl',
            name='tracking_id',
        ),
    ]