# Generated by Django 3.0.8 on 2020-07-26 21:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200726_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='ts',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 26, 17, 14, 4, 152988)),
        ),
    ]
