from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        editors, _ = Group.objects.get_or_create(name='editors')
        perm = Permission.objects.get(codename='view_secret_post')
        editors.permissions.add(perm)
        self.stdout.write(self.style.SUCCESS('Successfully added group'))
