from django.urls import path
from blog.apps import BlogConfig
from blog.views import PostListView, PostDetailView

app_name = BlogConfig.name

urlpatterns = [
    path("", PostListView.as_view(), name="blog"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post")
]
