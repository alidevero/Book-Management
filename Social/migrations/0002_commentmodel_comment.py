# Generated by Django 5.1.7 on 2025-03-15 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commentmodel',
            name='comment',
            field=models.TextField(default=None, max_length=500),
        ),
    ]
