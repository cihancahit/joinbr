from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied

from users.models import User


class ExpertRequiredMixin(LoginRequiredMixin):
    """Verify that the current Expert's user is logged user"""
    def dispatch(self, request, *args, **kwargs):
        if User.objects.filter(expert__slug=self.kwargs['slug']).exists():
            if not request.user == User.objects.get(expert__slug=self.kwargs['slug']):
                return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied()
