from django import template

register = template.Library()


@register.filter()
def format_path_to_image(text):
    return f'/media/{text}'
