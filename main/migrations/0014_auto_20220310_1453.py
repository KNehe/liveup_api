# Generated by Django 3.2 on 2022-03-10 11:53

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20220310_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='end_datetime',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 3, 10, 11, 53, 43, 457539, tzinfo=utc))]),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='start_datetime',
            field=models.DateTimeField(validators=[django.core.validators.MinValueValidator(datetime.datetime(2022, 3, 10, 11, 53, 43, 457539, tzinfo=utc))]),
        ),
    ]
