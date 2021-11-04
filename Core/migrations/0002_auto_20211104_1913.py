# Generated by Django 3.2.7 on 2021-11-04 19:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='date_birth__gte',
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('date_birth__gte', datetime.datetime(2021, 11, 4, 19, 13, 37, 530901, tzinfo=utc))), name='date_birth__gte'),
        ),
    ]