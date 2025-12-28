from django.urls import path

from club.views import ClubListView, ClubCreateView, ClubDetailView

app_name = 'club'

urlpatterns = [

    path('', ClubListView.as_view(), name='club_list'),
    path('create/', ClubCreateView.as_view(), name='club_create'),

    path('<slug:slug>/', ClubDetailView.as_view(), name='club_detail'),
]
