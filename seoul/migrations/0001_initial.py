# Generated by Django 2.1.2 on 2018-10-25 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('line_num', models.CharField(max_length=3)),
                ('station_cd', models.CharField(max_length=4, primary_key=True, serialize=False)),
                ('station_nm', models.CharField(max_length=20)),
                ('fr_code', models.CharField(max_length=5)),
            ],
        ),
    ]
