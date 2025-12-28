from django.urls import path

from membership.views import membership_request_create

app_name = 'membership'

urlpatterns = [
    path('request/<slug:slug>/', membership_request_create, name='request_create'),
]