# Generated by Django 3.2.7 on 2021-12-29 18:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_auto_20211215_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Data di creazione del modello', verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(blank=True, help_text='I tags che identificano il progetto', related_name='projects', related_query_name='projects', to='Core.Tag'),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(editable=False, help_text='Data di aggiornamento del modello', verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='role',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', related_query_name='roles', to='Core.project'),
        ),
        migrations.CreateModel(
            name='SearchCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, db_column='decription', null=True, verbose_name='description')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_cards', related_query_name='search_cards', to='Core.project')),
                ('skills', models.ManyToManyField(help_text='Le abilità richieste nella casta di ricerca', related_name='search_cards', related_query_name='search_cards', to='Core.Skill')),
            ],
            options={
                'verbose_name': 'Search Card',
                'verbose_name_plural': 'Search Cards',
                'db_table': 'search_card',
            },
        ),
    ]