# Generated by Django 4.2.4 on 2023-08-25 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Main_Database',
            fields=[
                ('data_id', models.AutoField(primary_key=True, serialize=False)),
                ('name_field', models.CharField(blank=True, max_length=200)),
                ('cost_field', models.CharField(blank=True, max_length=200)),
                ('time_field', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
