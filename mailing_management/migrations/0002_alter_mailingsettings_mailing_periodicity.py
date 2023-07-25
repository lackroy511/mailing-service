# Generated by Django 4.2.2 on 2023-07-25 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_management', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='mailing_periodicity',
            field=models.CharField(choices=[('M H * * *', 'Раз в день'), ('M H * * 1', 'Раз в неделю'), ('M H 1 * *', 'Раз в месяц')], max_length=40, verbose_name='периодичность'),
        ),
    ]
