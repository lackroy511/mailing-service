from django.shortcuts import redirect


class OwnerCheckMixin:
    def dispatch(self, request, *args, **kwargs):

        object = self.get_object()
        if object.user != self.request.user and not self.request.user.groups.filter(name='manager').exists() and not self.request.user.is_superuser:

            return redirect('mailing_management:index')

        return super().dispatch(request, *args, **kwargs)
