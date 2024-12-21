# Generated by Django 5.1.4 on 2024-12-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jira_dashboard', '0004_taskcomment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customusers',
            options={'ordering': ['-createdAt']},
        ),
        migrations.AlterUniqueTogether(
            name='customusers',
            unique_together={('phone', 'email', 'username')},
        ),
        migrations.AlterField(
            model_name='customusers',
            name='phone',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
        migrations.RemoveField(
            model_name='customusers',
            name='members',
        ),
    ]