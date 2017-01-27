import time

from sheep.models import Device, Flock, Sheep
from sheep.serializers import (
    DeviceSerializer,
    FlockSerializer,
    FlockAlertStatusSerializer,
    FlockCheckSerializer,
    SheepCheckSerializer,
    SheepSerializer
)
from sheep.sms import send_sms

from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

import logging
logger = logging.getLogger('Herd-It')


########################################
# Sites
########################################


def index(request):
    return render(request, "sheep/index.html")

########################################
# API Endpoints
########################################


# Get list of Bluetooth devices to scan for
class DeviceList(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = (AllowAny,)


class FlockCreateRetrieveUpdateView(mixins.RetrieveModelMixin,
                                    mixins.CreateModelMixin,
                                    generics.GenericAPIView):
    queryset = Flock.objects.all()
    serializer_class = FlockSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'flock_id'

    def get(self, request, flock_id):
        flock = get_object_or_404(Flock, flock_id=flock_id)
        sheep = flock.sheep()
        if sheep:
            serializer = SheepSerializer(sheep, many=True)
            return Response(serializer.data)
        else:
            return Response([])

    def post(self, request, flock_id):
        serializer = FlockSerializer(data=request.data)
        if serializer.is_valid():
            flocks = Flock.objects.filter(flock_id=flock_id)
            if len(flocks) > 0:
                flock = flocks[0]
                phone_number = serializer.data.get('phone_number', None)
                flock.phone_number = phone_number
                flock.save()
                return Response(serializer.data)
            else:
                serializer.save(flock_id=flock_id)
                return Response(serializer.data)
        else:
            return Response(serializer.data)


FLOCK_ALERT = 'FLOCK_ALERT'
SHEEP_ALERT = 'SHEEP_ALERT'
NO_ALERT = 'NO_ALERT'


# Get the status type of a flock
# FLOCK_ALERT or SHEEP_ALERT or NO_ALERT
class FlockAlertStatusView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, flock_id, format=None):
        flock = get_object_or_404(Flock, flock_id=flock_id)
        return Response(flock.alert_status())

    def post(self, request, flock_id, format=None):
        flock = get_object_or_404(Flock, flock_id=flock_id)
        serializer = FlockAlertStatusSerializer(data=request.data)
        if serializer.is_valid():
            state = serializer.data.get('state', False)
            flock.alert = state
            flock.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        logging.debug("Flock Alert Set to %s." % flock.alert)
        return Response(flock.alert_status())


class FoundFlock(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, flock_id, format=None):
        qpe = FlockCheckSerializer(data=request.query_params)
        latitude = None
        longitude = None
        if qpe.is_valid():
            latitude = qpe.validated_data.get('latitude', '')
            longitude = qpe.validated_data.get('longitude', '')
        else:
            logger.debug("Invalid query parameters")
            return Response(
                data={'detail': 'INVALID_MEAL_QUERY_PARAMS'},
                status=status.HTTP_400_BAD_REQUEST
            )

        flocks = Flock.objects.filter(flock_id=flock_id)
        if len(flocks) > 0:
            flock = flocks[0]
            if flock.alert:
                tel = flock.formatted_phone_number()
                logging.debug("Sending SMS to %s" % tel)
                date_time_stamp = time.strftime("%c")
                message = "Sheep from Flock Number %d last spotted at lat: %s, lon: %s at %s" % (flock.flock_id, latitude, longitude, date_time_stamp)
                response = send_sms(to=tel, message=message)
                logging.debug(response)

        return Response(
            data={'detail': 'SUCCESS'},
            status=status.HTTP_200_OK
        )


class FoundSheep(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        qpe = SheepCheckSerializer(data=request.query_params)

        if qpe.is_valid():
            flock_id = qpe.validated_data.get('flock_id', '')
            sheep_id = qpe.validated_data.get('sheep_id', '')
            latitude = qpe.validated_data.get('latitude', '')
            longitude = qpe.validated_data.get('longitude', '')

            flock = get_object_or_404(Flock, flock_id=flock_id)
            alert_status = flock.alert_status()
            if alert_status == FLOCK_ALERT:
                tel = flock.formatted_phone_number()
                logging.debug("Sending SMS to %s" % tel)
                date_time_stamp = time.strftime("%c")
                message = """
                    Sheep #%d from Flock #%d was last spotted at - lat: %s, lon: %s at %s. Map: http://maps.google.com/?ll=%s,%s
                    """ % (sheep_id, flock.flock_id, latitude, longitude, date_time_stamp, latitude, longitude)
                response = send_sms(to=tel, message=message)
                logging.debug(response)
                return Response(
                    data={'detail': 'SUCCESS'},
                    status=status.HTTP_200_OK
                )
            elif alert_status == SHEEP_ALERT:
                sheep = Sheep.objects.filter(sheep_id=sheep_id, flock__flock_id=flock_id)
                if len(sheep) > 0:
                    s = sheep[0]
                    if s.alert:
                        tel = flock.formatted_phone_number()
                        logging.debug("Sending SMS to %s" % tel)
                        date_time_stamp = time.strftime("%c")
                        message = """
                            Sheep #%d from Flock #%d was last spotted at - lat: %s, lon: %s at %s. Map: http://maps.google.com/?ll=%s,%s
                            """ % (s.sheep_id, flock.flock_id, latitude, longitude, date_time_stamp, latitude, longitude)
                        response = send_sms(to=tel, message=message)
                        logging.debug(response)
            return Response(
                data={'detail': 'SUCCESS'},
                status=status.HTTP_200_OK
            )
        else:
            logger.debug("Invalid query parameters")
            return Response(
                data={'detail': 'INVALID_MEAL_QUERY_PARAMS'},
                status=status.HTTP_400_BAD_REQUEST
            )
