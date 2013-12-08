import re

from tastypie.exceptions import Unauthorized
from tastypie.authorization import Authorization


class CommonAuthorization(Authorization):

    def is_authorized(self, request):
        if request.user.is_superuser:
            return True

        reg = re.search('/users/(?P<user_id>[1-9][0-9]*)/', request.path)
        if not reg:
            return False

        return int(reg.group('user_id')) == int(request.user.id)

    def read_list(self, object_list, bundle):
        if not self.is_authorized(bundle.request):
            raise Unauthorized()
        return object_list

    def read_detail(self, object_list, bundle):
        return self.is_authorized(bundle.request)

    def create_list(self, object_list, bundle):
        if not self.is_authorized(bundle.request):
            raise Unauthorized()
        return object_list

    def create_detail(self, object_list, bundle):
        return self.is_authorized(bundle.request)

    def update_list(self, object_list, bundle):
        if not self.is_authorized(bundle.request):
            raise Unauthorized()
        return object_list

    def update_detail(self, object_list, bundle):
        return self.is_authorized(bundle.request)

    def delete_list(self, object_list, bundle):
        if not self.is_authorized(bundle.request):
            raise Unauthorized()
        return object_list

    def delete_detail(self, object_list, bundle):
        return self.is_authorized(bundle.request)
