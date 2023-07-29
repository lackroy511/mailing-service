from django import template

register = template.Library()


@register.filter()
def max_len_str(text):
    return text[0:200] + '...'
