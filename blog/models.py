from pytils.translit import slugify

from django.db import models

from mailing_management.models import NULLABLE

# Create your models here.


class Post(models.Model):

    title = models.CharField(
        max_length=50, verbose_name='Заголовок')
    slug = models.SlugField(
        max_length=50, verbose_name='Слаг', unique=True, **NULLABLE)
    text = models.TextField(
        verbose_name='Текст поста')
    image = models.ImageField(
        upload_to='post_img', verbose_name='Изображение поста', **NULLABLE)
    views_count = models.PositiveIntegerField(
        verbose_name='Количество просмотров', default=0)
    published_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')

    def save(self, *args, **kwargs) -> None:
        self.slug = slugify(self.title)

        return super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-published_at']
