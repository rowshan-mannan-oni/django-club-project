from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView

from membership.models import MembershipRequest, Membership
from user.mixin import CustomLoginRequiredMixin
from .forms import ClubForm
from .models import Club

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
            if membership_request:
                context["membership_request_status"] = membership_request.status
            else:
                context["membership_request_status"] = None

            # User's membership role (if any)
            membership = Membership.objects.filter(user=user, club=self.object).first()
            if membership:
                context["user_role"] = membership.role
            else:
                context["user_role"] = None
        else:
            context["membership_request_status"] = None
            context["user_role"] = None

        return context
