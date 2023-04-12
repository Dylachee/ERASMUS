from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings


def create_activation_code(user):
    activation_code = get_random_string(10)
    user.activation_code = activation_code
    user.save()
    return activation_code


def send_activation_code(user, activation_link):
    message = f"""
    Спасибо за регистрацию! Пожалуйста, активируйте ваш аккаунт, перейдя по ссылке:
    {activation_link}
    """
    send_mail(
        subject='Активация аккаунта',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
