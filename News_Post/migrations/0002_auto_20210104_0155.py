# Generated by Django 3.1.3 on 2021-01-03 22:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('News_Post', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 4, 1, 55, 33, 450323)),
        ),
    ]
