# Generated by Django 4.2.2 on 2023-07-28 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('massage_subject', models.CharField(max_length=250, verbose_name='тема сообщения')),
                ('massage_text', models.TextField(verbose_name='текст сообщения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'Сообщение для рассылки',
                'verbose_name_plural': 'Сообщения для рассылки',
            },
        ),
        migrations.CreateModel(
            name='MailingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.TimeField(verbose_name='время рассылки')),
                ('end_mailing', models.DateTimeField(verbose_name='дата и время окончания рассылки')),
                ('mailing_periodicity', models.CharField(choices=[('M H * * *', 'Раз в день'), ('M H * * 1', 'Раз в неделю'), ('M H 1 * *', 'Раз в месяц')], max_length=40, verbose_name='периодичность в формате crontab')),
                ('mailing_periodicity_display', models.CharField(blank=True, max_length=40, null=True, verbose_name='периодичность')),
                ('mailing_status', models.CharField(choices=[('создана', 'Создана'), ('отправляется', 'Отправляется'), ('завершена', 'Завершена')], default='создана', max_length=20, verbose_name='cтатус')),
                ('mailing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mailing_management.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Настройки рассылки',
                'verbose_name_plural': 'Настройки рассылок',
                'ordering': ('mailing_status',),
            },
        ),
        migrations.CreateModel(
            name='MailingLogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_try_date', models.DateTimeField(auto_now=True, verbose_name='дата и время попытки')),
                ('try_status', models.CharField(max_length=10, verbose_name='статус попытки')),
                ('server_response', models.CharField(max_length=250, verbose_name='ответ сервера')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing_management.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Логи',
                'verbose_name_plural': 'Логи',
                'ordering': ('last_try_date',),
            },
        ),
    ]
