# from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post

# Create your views here.


class PostListView(ListView):
    model = Post
    extra_context = {
        'is_active_blog': 'active',
    }


class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.views_count += 1
        object.save()

        return object
