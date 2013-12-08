from django.contrib import admin
from django.conf.urls import patterns, include, url

from togile.api import togile_api


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^manage/', include(admin.site.urls)),
    url(r'^api/', include(togile_api.urls)),
)
