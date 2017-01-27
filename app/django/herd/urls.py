from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import TemplateView

from rest_framework.authtoken.views import obtain_auth_token

from sheep import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('sheep.urls', namespace='sheep')),

    # Index
    url(r'^$', TemplateView.as_view(template_name='sheep/index.html'), name='index'),

    # Rest Framework
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^token-auth/', obtain_auth_token),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
