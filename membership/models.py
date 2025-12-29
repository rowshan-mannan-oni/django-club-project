from django.db import models
from django.contrib.auth.models import User
from club.models import Club
from utils.choices import Role, RequestStatus

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='memberships')
    role = models.CharField(max_length=20, choices=Role, default=Role.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'memberships_membership'
        unique_together = ('user', 'club')
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.user.username} - {self.club.name} ({self.role})"

    @property
    def is_admin_or_moderator(self):
        return self.role == Role.ADMIN or self.role == Role.MODERATOR


class MembershipRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='membership_requests')
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='membership_requests')
    status = models.CharField(
        max_length=10,
        choices=RequestStatus,
        default=RequestStatus.PENDING
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reviewed_membership_requests'
    )

    class Meta:
        db_table = 'memberships_membership_request'
        unique_together = ('user', 'club')
        ordering = ['-requested_at']

    def __str__(self):
        return f"{self.user.username} -> {self.club.name} ({self.status})"
