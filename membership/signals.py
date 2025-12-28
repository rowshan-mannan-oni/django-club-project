from django.db.models.signals import post_save
from django.dispatch import receiver
from club.models import Club
from membership.models import Membership
from utils.choices import Role

@receiver(post_save, sender=Club)
def assign_creator_as_admin(instance, created, **kwargs):
    """
    When a club is created, make the creator its admin.
    """
    if created:
        Membership.objects.create(
            user=instance.created_by,
            club=instance,
            role=Role.ADMIN
        )