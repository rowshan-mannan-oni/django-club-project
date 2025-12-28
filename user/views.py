from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'user/signup_form.html'
    success_url = reverse_lazy('user:login')  # redirect here after successful signup

    def form_valid(self, form):

        user = form.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'user/login_form.html'
    def get_success_url(self):
        return reverse_lazy('club:club_list')
