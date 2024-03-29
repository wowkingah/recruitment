# Generated by Django 4.0.1 on 2022-11-12 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_alter_job_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='attachment',
            field=models.FileField(blank=True, upload_to='file/', verbose_name='简历附件'),
        ),
        migrations.AddField(
            model_name='resume',
            name='picture',
            field=models.ImageField(blank=True, upload_to='images/', verbose_name='个人照片'),
        ),
    ]
