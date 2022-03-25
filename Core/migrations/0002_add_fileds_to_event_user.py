# Generated by Django 3.2.12 on 2022-03-24 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default=None, max_length=64, null=True, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, editable=False),
        ),
    ]
