from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin:index')
        if not request.user.is_authenticated:
            return redirect('user:login')

        return super().dispatch(request, *args, **kwargs)
