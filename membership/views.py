from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import IntegerField, Case, When, Value
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from psycopg import Transaction

from club.models import Club
from membership.models import MembershipRequest, Membership
from user.mixin import CustomLoginRequiredMixin
from utils.choices import Role, RequestStatus


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

@login_required
def accept_membership_request(request, slug):
    club = get_object_or_404(Club, slug=slug)

    membership = get_object_or_404(
        Membership,
        user=request.user,
        club=club
    )

    if membership.role != Role.ADMIN:
        raise PermissionDenied

    if request.method != "POST":
        return redirect("membership:club_requests", slug=club.slug)

    request_id = request.POST.get("request_id")
    action = request.POST.get("action")

    membership_request = get_object_or_404(
        MembershipRequest,
        id=request_id,
        club=club
    )

    if membership_request.status != RequestStatus.PENDING:
        messages.warning(request, "This request has already been processed.")
        return redirect("membership:club_requests", slug=club.slug)

    if action == "accept":
        membership_request.status = RequestStatus.APPROVED
        Membership.objects.get_or_create(
            user=membership_request.user,
            club=club
        )
        messages.success(request, "Request accepted successfully!")

    elif action == "reject":
        membership_request.status = RequestStatus.REJECTED
        messages.info(request, "Membership rejected.")

    else:
        messages.error(request, "Invalid action.")
        return redirect("membership:club_requests", slug=club.slug)

    membership_request.reviewed_at = timezone.now()
    membership_request.reviewed_by = request.user
    membership_request.save()

    return redirect("membership:club_requests", slug=club.slug)


class ClubMembershipRequestListView(CustomLoginRequiredMixin, ListView):
    model = MembershipRequest
    template_name = "membership/club_requests.html"
    context_object_name = "membership_requests"

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, slug=kwargs["slug"])

        membership = Membership.objects.filter(user=request.user, club=self.club).first()
        if not membership or membership.role != Role.ADMIN:
            return HttpResponseForbidden("You are not allowed to view this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return (
            MembershipRequest.objects
            .filter(club=self.club)
            .order_by(
                Case(
                    When(status=RequestStatus.PENDING, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                ),
                "-requested_at",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["club"] = self.club
        return context


class MembershipListView(CustomLoginRequiredMixin, ListView):
    model = Membership
    template = "membership/membership_list.html"
    context_object_name = "memberships"

    def dispatch(self, request, *args, **kwargs):
        self.club = get_object_or_404(Club, slug=kwargs["slug"])

        membership = Membership.objects.filter(user=request.user, club=self.club).first()
        print(membership.role)
        if not membership:
            return HttpResponseForbidden("You are not allowed to view this page.")

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(club = self.club)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["club"] = self.club
        return context


@login_required
def change_role(request, slug, membership_id):
    club = get_object_or_404(Club, slug=slug)
    admin_membership = get_object_or_404(Membership, user=request.user, club=club)

    if admin_membership.role != Role.ADMIN:
        return HttpResponseForbidden("Only admins can change roles.")

    membership = get_object_or_404(Membership, id=membership_id, club=club)

    if membership.role == Role.ADMIN or membership.user == request.user:
        messages.warning(request, "You cannot change this member's role.")
        return redirect("membership:membership_list", slug=club.slug)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "promote" and membership.role == Role.MEMBER:
            membership.role = Role.MODERATOR
            membership.save()
            messages.success(request, f"{membership.user.username} promoted to Moderator.")

        elif action == "demote" and membership.role == Role.MODERATOR:
            membership.role = Role.MEMBER
            membership.save()
            messages.success(request, f"{membership.user.username} demoted to Member.")

        else:
            messages.error(request, "Invalid action or role transition.")

    return redirect("membership:membership_list", slug=club.slug)