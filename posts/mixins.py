from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Post

class HasPermissionToPost(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.info(request, 'Sorry, you do no have permission to post, please contact admin!')
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)



class PostPermissionRequiredMixin(PermissionRequiredMixin):
    """Verify that the current user has all specified permissions."""
    permission_required = 'posts.author'

    def get_permission_denied_message(self):
        """
        Override this method to override the permission_denied_message attribute.
        """
        messages.info(self.request, 'You have no permission!')
        return self.permission_denied_message
   