from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from togile.api import togile_api


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'togile.apps.todo.views.index_view'),
    url(r'^logout/$', 'togile.apps.todo.views.logout_view'),
    url(r'^manage/', include(admin.site.urls)),
    url(r'^api/', include(togile_api.urls)),
    url('', include('social.apps.django_app.urls', namespace='social')),
)

urlpatterns += staticfiles_urlpatterns()
