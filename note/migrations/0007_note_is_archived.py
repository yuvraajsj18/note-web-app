# Generated by Django 3.1 on 2020-10-15 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0006_note_datetime'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
