# Generated by Django 3.1 on 2020-10-12 13:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('note', '0005_auto_20200924_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
