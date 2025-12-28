from django.db import models
from django.contrib.auth.models import User
from club.models import Club
from utils.choices import PostType

class Post(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    type = models.CharField(
        max_length=10,
        choices=PostType,
        default=PostType.BLOG
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    class Meta:
        db_table = 'posts_post'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.type})"
