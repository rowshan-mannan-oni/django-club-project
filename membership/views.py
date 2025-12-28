from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView

from club.models import Club
from membership.models import MembershipRequest, Membership
from user.mixin import CustomLoginRequiredMixin
from utils.choices import Role


@login_required
def membership_request_create(request, slug):
    club = get_object_or_404(Club, slug=slug)

    # Check if user is already a member or has a pending request
    existing_request = MembershipRequest.objects.filter(user=request.user, club=club).exists()
    if existing_request:
        messages.info(request, "You already requested membership for this club.")
        return redirect('club:club_detail', slug=club.slug)

    # Create membership request
    MembershipRequest.objects.create(user=request.user, club=club)
    messages.success(request, "Membership request sent successfully!")
    return redirect('club:club_detail', slug=club.slug)


class ClubMembershipRequestListView(CustomLoginRequiredMixin, ListView):
    model = MembershipRequest
    template_name = "membership/club_requests.html"
    context_object_name = "membership_requests"

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, slug=kwargs["slug"])

        membership = Membership.objects.filter(user=request.user, club=self.club).first()
        if not membership or membership.role not in [Role.ADMIN, Role.MODERATOR]:
            return HttpResponseForbidden("You are not allowed to view this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Only requests for this club
        return MembershipRequest.objects.filter(club=self.club).order_by("-requested_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["club"] = self.club
        return context
