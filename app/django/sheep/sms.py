from django.conf import settings
from twilio.rest import TwilioRestClient


def send_sms(to, message):
    client = TwilioRestClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(to=to, from_=settings.TWILIO_FROM_NUMBER, body=message)
    return message
