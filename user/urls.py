from django.contrib.auth import views
from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy

from user.views import SignUpView, CustomLoginView

app_name = 'user'

urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(next_page='club:club_list'), name="logout"),
]
