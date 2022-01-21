# Generated by Django 3.2.7 on 2022-01-20 18:14
from ..models.Projects.MessageFile import file_path
from django.conf import settings
from django.db import migrations, models
import Core.models.Projects.Project
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0004_initial_showcase'),
    ]

    operations = [
        migrations.AddField(
            model_name='showcase',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='showcases_created', related_query_name='showcases_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=1000, upload_to=file_path)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', related_query_name='files', to='Core.message')),
            ],
            options={
                'verbose_name': 'MessageFile',
                'verbose_name_plural': 'MessageFiles',
                'db_table': 'message_file',
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=Core.models.Projects.Project.image_path, verbose_name='image'),
        ),
    ]
