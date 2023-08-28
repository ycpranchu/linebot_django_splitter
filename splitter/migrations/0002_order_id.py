# Generated by Django 4.2.4 on 2023-08-28 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('splitter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_ID',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField(blank=True)),
                ('Main_Database', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='splitter.main_database')),
            ],
        ),
    ]
