# Generated by Django 4.2.18 on 2025-05-30 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('conversation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='conversationmessage',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
