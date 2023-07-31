from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


class OwnerCheckMixin:
    def dispatch(self, request, *args, **kwargs):

        object = self.get_object()
        if object.user != self.request.user and not self.request.user.groups.filter(name='manager').exists() and not self.request.user.is_superuser:

            return redirect('mailing_management:index')

        return super().dispatch(request, *args, **kwargs)


class CacheViewMixin:

    @method_decorator(cache_page(30))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
