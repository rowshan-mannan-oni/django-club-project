from django.urls import path

from membership.views import membership_request_create, ClubMembershipRequestListView

app_name = 'membership'

urlpatterns = [
    path('request/<slug:slug>/', membership_request_create, name='request_create'),
    path('club/<slug:slug>/requests/', ClubMembershipRequestListView.as_view(), name='club_requests'),
]