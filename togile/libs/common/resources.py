from django.core.urlresolvers import resolve


from tastypie.resources import Bundle
from tastypie.serializers import Serializer
from tastypie.resources import ModelResource
from tastypie.authentication import SessionAuthentication

from togile.libs.common.auth import CommonAuthorization


class CommonModelResource(ModelResource):

    def base_urls(self):
        """
        Remove base urls
        """
        return list()

    def resource_uri_kwargs(self, bundle_or_obj=None):
        kwargs = super(CommonModelResource, self).resource_uri_kwargs(
            bundle_or_obj)

        if isinstance(bundle_or_obj, Bundle):
            resolved = resolve(bundle_or_obj.request.path)
            kwargs.update(resolved.kwargs)

        return kwargs


class CommonMeta(object):
    # excludes = ['id']
    authentication = SessionAuthentication()
    authorization = CommonAuthorization()
    serializer = Serializer(formats=['json'])
