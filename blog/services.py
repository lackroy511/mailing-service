from django.core.cache import cache
from config.settings import CACHE_ENABLED

from blog.models import Post


def get_cached_posts():
    """Получить список постов из кеша, если необходимо, то из БД."""

    if CACHE_ENABLED:
        key = 'blog_posts_list'
        cached_posts = cache.get(key)
        if cached_posts is None:
            queryset = Post.objects.all()
            cache.set(key, queryset, 30)
    else:
        queryset = Post.objects.all()

    return queryset
