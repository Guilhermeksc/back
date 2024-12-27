from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_validation_email(email, validation_url):
    """
    Tarefa para enviar o e-mail de validação.
    """
    send_mail(
        subject="Valide seu registro",
        message=f"Por favor, clique no link para validar sua conta: {validation_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
    )
