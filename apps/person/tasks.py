import logging
import smtplib
import requests
import json

from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import BadHeaderError, EmailMultiAlternatives

# Celery config
from celery import shared_task


@shared_task
def send_verifycode_email(data):
    logging.info(_("Send verifyCode email run"))

    to = data.get('email', None)
    passcode = data.get('passcode', None)

    if to and passcode:
        subject = _("Kode Verifiaksi")
        from_email = '%s <noreply@mydomain.com>' % (settings.APP_NAME)

        # Message
        text = 'Kode Verifikasi Storee Barber %s Jangan berikan kode OTP kepada siapapun!' % passcode
        html = text

        if subject and from_email:
            try:
                msg = EmailMultiAlternatives(subject, text, from_email, [to])
                msg.attach_alternative(html, "text/html")
                msg.send()
                logging.info(_("VerifyCode email success"))
            except smtplib.SMTPConnectError as e:
                logging.error('SMTPConnectError: %s' % e)
            except smtplib.SMTPAuthenticationError as e:
                logging.error('SMTPAuthenticationError: %s' % e)
            except smtplib.SMTPSenderRefused as e:
                logging.error('SMTPSenderRefused: %s' % e)
            except smtplib.SMTPRecipientsRefused as e:
                logging.error('SMTPRecipientsRefused: %s' % e)
            except smtplib.SMTPDataError as e:
                logging.error('SMTPDataError: %s' % e)
            except smtplib.SMTPException as e:
                logging.error('SMTPException: %s' % e)
            except BadHeaderError:
                logging.warning(_("Invalid header found"))
    else:
        logging.warning(
            _("Tried to send email to non-existing VerifyCode Code"))


@shared_task
def send_verifycode_msisdn(data):
    logging.info(_("Send verifyCode msisdn run"))

    to = data.get('msisdn', None)
    passcode = data.get('passcode', None)

    if to and passcode:
        url = 'https://api.zuwinda.com/v1/message/send-sms'
        payload = {
            "content": "Kode Verifikasi Storee Barber % s Jangan berikan kode OTP kepada siapapun!" % passcode,
            "to": to
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x-access-key': '928cfa5aac984a1c93bdd24da5dee441'
        }
        r = requests.post(url, json=payload, headers=headers)
        logging.info(r.status_code)
    else:
        logging.warning(
            _("Tried to send email to non-existing VerifyCode Code"))
