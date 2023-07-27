from django.shortcuts import redirect


class OwnerCheckMixin:
    def dispatch(self, request, *args, **kwargs):

        object = self.get_object()
        if object.user != self.request.user:

            return redirect('mailing_management:index')

        return super().dispatch(request, *args, **kwargs)
