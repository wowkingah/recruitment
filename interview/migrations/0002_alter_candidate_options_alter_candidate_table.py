# Generated by Django 4.0.1 on 2022-01-22 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'verbose_name': '应聘者', 'verbose_name_plural': '应聘者'},
        ),
        migrations.AlterModelTable(
            name='candidate',
            table='candidate',
        ),
    ]