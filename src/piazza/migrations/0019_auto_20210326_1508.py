# Generated by Django 3.0 on 2021-03-26 15:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('piazza', '0018_auto_20210326_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 15, 8, 5, 879197)),
        ),
    ]