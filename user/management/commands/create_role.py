from django.contrib.auth.models import Group
from django.core.management import BaseCommand

from utils.choices import Role

class Command(BaseCommand):
    name = 'assign_role'
    help = 'Create groups and permissions'

    def handle(self, *args, **options):
        admin_group, created = Group.objects.get_or_create(name=Role.ADMIN)
        moderator_group, created = Group.objects.get_or_create(name=Role.MODERATOR)
        member_group, created = Group.objects.get_or_create(name=Role.MEMBER)

        print("Successfully created roles:")
        for role in Group.objects.all():
            print(f"- {role.name}")
