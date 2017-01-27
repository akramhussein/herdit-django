from datetime import date, timedelta

from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.core.validators import MinValueValidator, MaxValueValidator

from sheep.utilities import formatted_tel

from .haversine import haversine


MIN_MINOR_MINOR = 1
MAX_MAJOR_MINOR = 65535

import logging
logger = logging.getLogger('Herd-It')


class Device(TimeStampedModel):
    uuid = models.CharField(unique=True, max_length=1024, null=False, blank=False)
    comment = models.CharField(max_length=1024, null=False, blank=False)

    def __unicode__(self):
        return self.uuid

FLOCK_ALERT = 'FLOCK_ALERT'
SHEEP_ALERT = 'SHEEP_ALERT'
NO_ALERT = 'NO_ALERT'


class Flock(TimeStampedModel):
    flock_id = models.IntegerField(
        unique=True,
        null=False,
        blank=False,
        validators=[
            MinValueValidator(MIN_MINOR_MINOR),
            MaxValueValidator(MAX_MAJOR_MINOR)
        ])

    phone_number = models.CharField(max_length=20, null=True, blank=True)
    comment = models.CharField(max_length=1024, null=True, blank=True)
    alert = models.BooleanField(default=False)

    def __unicode__(self):
        return "%d" % self.flock_id

    def formatted_phone_number(self):
        return formatted_tel(self.phone_number)

    def sheep(self):
        return Sheep.objects.filter(flock__flock_id=self.flock_id)

    def alert_status(self):
        if self.alert:
            logging.debug("Flock Alert Set %s" % self.alert)
            return FLOCK_ALERT

        sheep = Sheep.objects.filter(flock__flock_id=self.flock_id)
        sheep_alert_set = False
        for s in sheep:
            if s.alert:
                sheep_alert_set = True

        if sheep_alert_set:
            return SHEEP_ALERT

        return NO_ALERT


class Sheep(TimeStampedModel):
    flock = models.ForeignKey(Flock, null=False, blank=False)
    sheep_id = models.IntegerField(
        null=False,
        blank=False,
        validators=[
            MinValueValidator(MIN_MINOR_MINOR),
            MaxValueValidator(MAX_MAJOR_MINOR)
        ])

    comment = models.CharField(unique=True, max_length=1024, null=True, blank=True)
    alert = models.BooleanField(default=False)

    def __unicode__(self):
        return "%d (FLOCK: %d)" % (self.sheep_id, self.flock.id)

######################################################################
# Token Auth
######################################################################

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
