# from django.shortcuts import render
from blog.services import get_cached_posts
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Post

# Create your views here.


class PostListView(ListView):
    model = Post
    extra_context = {
        'is_active_blog': 'active',
    }

    def get_queryset(self):
        return get_cached_posts()


class PostDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    model = Post
    permission_required = 'blog.view_post'

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.views_count += 1
        object.save()

        return object
