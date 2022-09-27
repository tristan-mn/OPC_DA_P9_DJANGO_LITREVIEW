from django.template import Library

register = Library()

@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_poster_display(context, user):
    if context['user'] == user:
        return 'vous'
    return user.username
