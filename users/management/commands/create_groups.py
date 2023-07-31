from django.core.management import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='manager')

        permissions = [
            Permission.objects.get(codename='view_mailing'),
            Permission.objects.get(codename='change_mailing'),
            Permission.objects.get(codename='add_mailing'),
            Permission.objects.get(codename='view_mailingsettings'),
            Permission.objects.get(codename='add_mailingsettings'),
            Permission.objects.get(codename='change_mailingsettings'),
            Permission.objects.get(codename='view_user'),
            Permission.objects.get(codename='change_user'),
            Permission.objects.get(codename='view_post'),
        ]
        group.permissions.set(permissions)

        group, created = Group.objects.get_or_create(name='standart-user')

        permissions = [
            Permission.objects.get(codename='add_client'),
            Permission.objects.get(codename='change_client'),
            Permission.objects.get(codename='delete_client'),
            Permission.objects.get(codename='view_client'),
            Permission.objects.get(codename='add_mailing'),
            Permission.objects.get(codename='change_mailing'),
            Permission.objects.get(codename='delete_mailing'),
            Permission.objects.get(codename='view_mailing'),
            Permission.objects.get(codename='view_mailinglogs'),
            Permission.objects.get(codename='add_mailingsettings'),
            Permission.objects.get(codename='change_mailingsettings'),
            Permission.objects.get(codename='delete_mailingsettings'),
            Permission.objects.get(codename='view_mailingsettings'),
            Permission.objects.get(codename='view_post'),
        ]
        group.permissions.set(permissions)

        group, created = Group.objects.get_or_create(name='content-manager')

        permissions = [
            Permission.objects.get(codename='add_post'),
            Permission.objects.get(codename='change_post'),
            Permission.objects.get(codename='delete_post'),
            Permission.objects.get(codename='view_post'),
        ]
        group.permissions.set(permissions)
