import datetime

from django.conf import settings
from django.core.mail import send_mail

from client.models import Logi, Newsletter


def _send(newsletter, message_client):
    result = send_mail(
        subject=newsletter.message.topic,
        message=newsletter.message.message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[message_client.email],
        fail_silently=False
    )

    Logi.objects.create(
        status=Logi.STATUS_OK if result else Logi.STATUS_FAILED,
        settings=newsletter,
        client_id=message_client.pk
    )


def send_mails():
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    for newsletter in Newsletter.objects.filter(status=Newsletter.STATUS_STARTED):
        if (datetime_now > newsletter.start_time) and (datetime_now < newsletter.end_time):
            for newsletter_client in newsletter.client.all():
                logi = Logi.objects.filter(
                    client=newsletter_client.pk,
                    settings=newsletter
                )
                if logi.exists():
                    last_try_date = logi.order_by('-last').first()

                    if newsletter.period == Newsletter.PERIOD_DAILY:
                        if (datetime_now - last_try_date).days >= 1:
                            _send(newsletter, newsletter_client)
                    elif newsletter.period == Newsletter.PERIOD_WEEKLY:
                        if (datetime_now - last_try_date).days >= 7:
                            _send(newsletter, newsletter_client)
                    elif newsletter.period == Newsletter.PERIOD_MONTHLY:
                        if (datetime_now - last_try_date).days >= 30:
                            _send(newsletter, newsletter_client)
                else:
                    _send(newsletter, newsletter_client)
