from typing import cast, Iterable, Any

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from post.models import Post
from club.models import Club
from membership.models import Membership
from utils.choices import PostType


class PostCreateView(CreateView):
    model = Post
    template_name = "post/post_form.html"
    fields = ["type", "title", "content", "is_published"]

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, slug=kwargs.get("slug"))

        membership = Membership.objects.filter(
            user=request.user, club=self.club, is_active=True
        ).first()

        if not membership:
            raise PermissionDenied("You must be a club member to create a post.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.club = self.club

        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("club:club_detail", kwargs={"slug": self.club.slug})
