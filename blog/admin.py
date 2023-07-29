from django.contrib import admin

from blog.models import Post

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'published_at')
    list_filter = ('published_at',)
    search_fields = ('title',)
