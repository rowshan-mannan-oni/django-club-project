from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect

from club.models import Club
from membership.models import MembershipRequest

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
