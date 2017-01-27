from sheep.models import Device, Flock, Sheep

from rest_framework import serializers

import logging
logger = logging.getLogger('Herd-It')


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = (
            'id',
            'created',
            'modified'
        )


class FlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flock
        exclude = (
            'id',
            'created',
            'modified',
            'comment',
            'flock_id',
            'alert'
        )


class SheepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheep
        exclude = (
            'id',
            'created',
            'modified',
            'comment'
        )


class FlockAlertStatusSerializer(serializers.Serializer):
    state = serializers.BooleanField(required=True)


class FlockCheckSerializer(serializers.Serializer):
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)


class SheepCheckSerializer(serializers.Serializer):
    flock_id = serializers.IntegerField(required=True)
    sheep_id = serializers.IntegerField(required=True)
    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
