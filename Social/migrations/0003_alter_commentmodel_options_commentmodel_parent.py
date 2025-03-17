# Generated by Django 5.1.7 on 2025-03-15 18:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Social', '0002_commentmodel_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentmodel',
            options={'ordering': ['commented_at']},
        ),
        migrations.AddField(
            model_name='commentmodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='Social.commentmodel'),
        ),
    ]
