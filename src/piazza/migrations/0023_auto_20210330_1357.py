# Generated by Django 3.0 on 2021-03-30 13:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0022_auto_20210330_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 30, 13, 57, 31, 558209, tzinfo=utc)),
        ),
    ]
