# Generated by Django 5.1.4 on 2024-12-20 06:05

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customusers',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=256, unique=True),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(null=True)),
                ('deassignee', models.BooleanField(default=False)),
                ('storyPoint', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jira_dashboard.project')),
            ],
            options={
                'db_table': 'task',
            },
        ),
    ]
