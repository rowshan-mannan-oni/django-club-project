from django.db import models
from django.utils.translation import gettext_lazy as _

class Role(models.TextChoices):
    ADMIN = 'CLUB_ADMIN', _('Club Admin')
    MODERATOR = 'CLUB_MODERATOR', _('Club Moderator')
    MEMBER = 'CLUB_MEMBER', _('Club Member')

class RequestStatus(models.TextChoices):
    PENDING = 'PENDING', _('Pending')
    APPROVED = 'APPROVED', _('Approved')
    REJECTED = 'REJECTED', _('Rejected')

class PostType(models.TextChoices):
    BLOG = 'BLOG', _('Blog')
    NEWS = 'NEWS', _('News')