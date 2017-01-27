from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from sheep import views

urlpatterns = [
    # Returns list of Bluetooth devices
    url(r'^devices/$', views.DeviceList.as_view(), name='device_list'),
    url(r'^flock/(?P<flock_id>[0-9A-Za-z]+)$', views.FlockCreateRetrieveUpdateView.as_view(), name='flock_create_or_update'),

    # Notify when found a flock or sheep
    url(r'^found/flock/(?P<flock_id>[0-9A-Za-z]+)/?$', views.FoundFlock.as_view(), name='found_flock'),
    url(r'^found/sheep/?$', views.FoundSheep.as_view(), name='found_sheep'),

    # Returns status of Flock: FLOCK_ALERT, SHEEP_ALERT, NO_ALERT
    url(r'^status/(?P<flock_id>[0-9A-Za-z]+)$', views.FlockAlertStatusView.as_view(), name='flock_alert_status'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
