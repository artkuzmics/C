# Generated by Django 3.0 on 2021-03-26 10:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0010_auto_20210326_1020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 10, 28, 51, 778766, tzinfo=utc)),
        ),
    ]