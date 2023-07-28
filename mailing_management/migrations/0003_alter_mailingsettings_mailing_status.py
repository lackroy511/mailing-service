# Generated by Django 4.2.2 on 2023-07-28 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing_management', '0002_rename_end_mailing_mailingsettings_end_mailing_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailingsettings',
            name='mailing_status',
            field=models.CharField(choices=[('создана', 'Создана'), ('отправляется', 'Отправляется'), ('завершена', 'Завершена'), ('устарела', 'Устарела')], default='создана', max_length=20, verbose_name='cтатус'),
        ),
    ]
