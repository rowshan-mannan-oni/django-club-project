from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView

from membership.models import MembershipRequest, Membership
from post.models import Post
from user.mixin import CustomLoginRequiredMixin
from .forms import ClubForm
from .models import Club
from utils.choices import RequestStatus, PostType

from django.core.paginator import Paginator
class ClubListView(generic.ListView):
    model = Club
    context_object_name = 'clubs'
    paginate_by = 10

class ClubCreateView(CustomLoginRequiredMixin, CreateView):
    model = Club
    template_name = 'club/club_form.html'
    success_url = reverse_lazy('club:club_list')
    form_class = ClubForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ClubDetailView(DetailView):
    model = Club
    template_name = 'club/club_detail.html'
    context_object_name = 'club'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Membership request status for join button
        if user.is_authenticated:
            membership_request = MembershipRequest.objects.filter(user=user, club=self.object).first()
            context["membership_request_status"] = membership_request.status if membership_request else None

            membership = Membership.objects.filter(user=user, club=self.object).first()
            context["user_role"] = membership.role if membership else None
        else:
            context["membership_request_status"] = None
            context["user_role"] = None

        # Separate posts by type
        blog_posts = Post.objects.filter(club=self.object, type=PostType.BLOG).order_by('-created_at')
        news_posts = Post.objects.filter(club=self.object, type=PostType.NEWS).order_by('-created_at')

        # Pagination
        blog_page = self.request.GET.get('blog_page', 1)
        news_page = self.request.GET.get('news_page', 1)

        blog_paginator = Paginator(blog_posts, 5)
        news_paginator = Paginator(news_posts, 5)

        context["blog_posts"] = blog_paginator.get_page(blog_page)
        context["news_posts"] = news_paginator.get_page(news_page)

        context["RequestStatus"] = RequestStatus
        return context
