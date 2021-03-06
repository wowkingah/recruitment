# Generated by Django 4.0.1 on 2022-01-23 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_alter_candidate_options_alter_candidate_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='first_professional_competency',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, verbose_name='专业能力得分'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='first_learning_ability',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=2, null=True, verbose_name='学习能力得分'),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='second_interviewer',
            field=models.CharField(blank=True, max_length=256, verbose_name='二面面试官'),
        ),
    ]
