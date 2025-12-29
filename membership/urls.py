from django.urls import path

from membership.views import membership_request_create, ClubMembershipRequestListView, accept_membership_request, \
    MembershipListView, change_role

app_name = 'membership'

urlpatterns = [
    path('request/<slug:slug>/', membership_request_create, name='request_create'),
    path('club/<slug:slug>/requests/', ClubMembershipRequestListView.as_view(), name='club_requests'),
    path("clubs/<slug:slug>/requests/action/", accept_membership_request, name="membership_request_action"),
    path("clubs/<slug:slug>/members/", MembershipListView.as_view(), name="membership_list"),
    path("clubs/<slug:slug>/members/<int:membership_id>/role/", change_role, name="change_role")
]
