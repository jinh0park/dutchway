# Generated by Django 2.1.2 on 2018-11-01 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seoul', '0007_auto_20181031_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='station',
            name='head_time',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='station',
            name='tail_time',
            field=models.FloatField(null=True),
        ),
    ]