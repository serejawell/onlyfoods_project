from django import template

register = template.Library()

@register.filter()
def media_filter(path):
    if path:
        return f'/media/{path}'
    return '#'

@register.filter()
def is_following(user, target_user):
    """Проверяет, подписан ли пользователь на другого"""
    if user.is_authenticated:
        return user.is_following(target_user)
    return False