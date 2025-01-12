from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from onlyfoods import settings


def send_welcome_email(user, url):
    '''Приветственное письмо при регистрации'''
    html_content = render_to_string('users/welcome_email.html', {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'url': url,
    })
    text_content = strip_tags(html_content)

    # Отправляем письмо
    email = EmailMultiAlternatives(
        subject='Welcome to the Serega Agency!',
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email],
    )
    email.attach_alternative(html_content, "text/html")  # Добавляем HTML-версию
    email.send(fail_silently=False)