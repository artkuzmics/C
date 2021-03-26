# Generated by Django 3.0 on 2021-03-26 09:55

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('piazza', '0004_auto_20210326_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_author', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='post',
            name='expiration',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 26, 10, 0, 44, 243074, tzinfo=utc)),
        ),
    ]
