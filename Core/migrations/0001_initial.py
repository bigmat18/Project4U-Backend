# Generated by Django 3.2.7 on 2021-11-04 19:13

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(blank=True, max_length=30)),
                ('last_name', models.CharField(blank=True, max_length=150)),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
                'db_table': 'email',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(help_text='Testo del modello', verbose_name='text')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, help_text='Data di creazione del modello', verbose_name='created at')),
                ('updated_at', models.DateTimeField(help_text='Data di aggiornamento del modello', verbose_name='updated at')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('link_site', models.CharField(blank=True, help_text='Link del sito di contatto del progetto', max_length=516, null=True, verbose_name='link site')),
                ('ended_at', models.DateTimeField(blank=True, help_text='Data di chiusura del progetto. Se null il progetto è aperto', null=True, verbose_name='ended')),
                ('num_swipe', models.PositiveBigIntegerField(default=0, help_text='Il numero di swipe fatti dal progetto', verbose_name='number swipe')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'db_table': 'project',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('type_skill', models.CharField(choices=[('Programming', 'Programming'), ('Managment', 'Management'), ('Design', 'Design'), ('Other', 'Other')], default='Other', max_length=64, verbose_name='type skill')),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
                'db_table': 'skill',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('searches_number', models.PositiveIntegerField(default=0, help_text='Numero di ricerche fatte a questo tag', verbose_name='searches number')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('level', models.PositiveIntegerField(default=1, help_text="Livello di competenza della skill dell'utente", validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.skill')),
            ],
            options={
                'verbose_name': 'User Skill',
                'verbose_name_plural': 'Users Skills',
                'db_table': 'user_skill',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='slug')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='image')),
                ('username', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('date_birth', models.DateField(blank=True, null=True, verbose_name='date birth')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('active', models.BooleanField(default=True, verbose_name='is active')),
                ('blocked', models.BooleanField(default=False, help_text='Indica se un utente è stato bloccato.', verbose_name='is blocked')),
                ('admin', models.BooleanField(default=False, verbose_name='is admin')),
                ('type_user', models.CharField(choices=[('01', 'Base'), ('02', 'Verified'), ('03', 'Innovator')], default='01', max_length=64, verbose_name='type user')),
                ('type_vip', models.CharField(choices=[('FREE', 'Free'), ('LV1', 'Level 01'), ('LV2', 'Level 02'), ('LV3', 'Level 03')], default='FREE', max_length=64, verbose_name='type vip')),
                ('highscool', models.CharField(blank=True, help_text='La scuola superiori frequentata', max_length=256, null=True, verbose_name='highscool')),
                ('university', models.CharField(blank=True, help_text="L'università frequentata", max_length=256, null=True, verbose_name='university')),
                ('extra', models.TextField(blank=True, help_text='Le esperienze scolasti o non, extra dello user', null=True, verbose_name='extra')),
                ('project_saved', models.ManyToManyField(related_name='saved_by', related_query_name='saved_by', to='Core.Project')),
                ('skills', models.ManyToManyField(related_name='users', related_query_name='users', through='Core.UserSkill', to='Core.Skill')),
                ('user_saved', models.ManyToManyField(related_name='_Core_user_user_saved_+', related_query_name='saved_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='userskill',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserProject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now, help_text='Data di aggiunta utente nel progetto', verbose_name='date added')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.project')),
                ('role', models.ManyToManyField(help_text="Elenco dei ruoli dell'utente all'interno del progetto", related_name='users', related_query_name='users', to='Core.Role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Project',
                'verbose_name_plural': 'User Projects',
                'db_table': 'user_project',
                'ordering': ['-date_added'],
            },
        ),
        migrations.AddField(
            model_name='role',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', related_query_name='roles', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_created', related_query_name='projects_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(help_text='I tags che identificano il progetto', related_name='projects', related_query_name='projects', to='Core.Tag'),
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='projects', related_query_name='projects', through='Core.UserProject', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('date_birth__gte', datetime.datetime(2021, 11, 4, 19, 13, 4, 842083, tzinfo=utc))), name='date_birth__gte'),
        ),
        migrations.AlterUniqueTogether(
            name='userskill',
            unique_together={('skill', 'user')},
        ),
        migrations.AddIndex(
            model_name='userproject',
            index=models.Index(fields=['-date_added'], name='user_projec_date_ad_00e3da_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='userproject',
            unique_together={('user', 'project')},
        ),
    ]
