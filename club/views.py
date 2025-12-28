from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DetailView

from membership.models import MembershipRequest
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

        membership_request_status = None

        if user.is_authenticated:
            membership_request_status = MembershipRequest.objects.filter(
                user=user, club=self.object
            ).values_list('status', flat=True).first()

        context['membership_request_status'] = membership_request_status

        return context
