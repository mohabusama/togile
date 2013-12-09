from django.conf.urls import url

from tastypie import fields
from tastypie.validation import Validation

from togile.apps.todo.models import TodoList, TodoItem
from togile.libs.common.resources import CommonModelResource, CommonMeta


class TodoListValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Invalid Input Data!'}

        errors = {}
        if bundle.request.method == 'POST' and not bundle.data.get('title'):
            errors['title'] = 'A Todo List must have a Title!'

        return errors


class TodoItemValidation(Validation):
    def is_valid(self, bundle, request=None):
        if not bundle.data:
            return {'__all__': 'Invalid Input Data!'}

        errors = {}
        if bundle.request.method == 'POST' and not bundle.data.get('value'):
            errors['value'] = 'A Todo Item must have a Value (Text)!'

        return errors


class TodoListResource(CommonModelResource):

    user_id = fields.IntegerField(attribute='user_id')
    parent_id = fields.IntegerField(attribute='parent_id', null=True)

    class Meta(CommonMeta):
        queryset = TodoList.objects.select_related('user').all()

        resource_name = 'lists'

        always_return_data = True

        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']

        limit = 50

        filtering = {
            'user_id': ('exact')
        }

        validation = TodoListValidation()

    def dispatch(self, request_type, request, **kwargs):
        kwargs['user_id'] = kwargs.pop('user__id')

        return super(TodoListResource, self).dispatch(
            request_type, request, **kwargs)

    def prepend_urls(self):
        return [
            url(r'^users/(?P<user__id>[1-9][0-9]*)/(?P<resource_name>%s)/$' %
                self._meta.resource_name,
                self.wrap_view('dispatch_list'),
                name='api_dispatch_list'),
            url(r'^users/(?P<user__id>[1-9][0-9]*)/(?P<resource_name>%s)/'
                '(?P<pk>[1-9][0-9]*)/$' % self._meta.resource_name,
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail')
        ]


class TodoItemResource(CommonModelResource):

    todo_list_id = fields.IntegerField(attribute='todo_list_id')

    class Meta(CommonMeta):
        queryset = TodoItem.objects.select_related('todo_list', 'user').all()

        resource_name = 'todos'

        always_return_data = True

        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get', 'put', 'delete']

        limit = 1000

        filtering = {
            'user_id': ('exact'),
            'todo_list_id': ('exact')
        }

        validation = TodoItemValidation()

    def dispatch(self, request_type, request, **kwargs):
        kwargs.pop('user_id')
        kwargs['todo_list_id'] = kwargs.pop('todo_list__id')

        return super(TodoItemResource, self).dispatch(
            request_type, request, **kwargs)

    def prepend_urls(self):
        return [
            url(r'^users/(?P<user_id>[1-9][0-9]*)/lists/'
                '(?P<todo_list__id>[1-9][0-9]*)/(?P<resource_name>%s)/$' %
                self._meta.resource_name,
                self.wrap_view('dispatch_list'),
                name='api_dispatch_list'),
            url(r'^users/(?P<user_id>[1-9][0-9]*)/lists/'
                '(?P<todo_list__id>[1-9][0-9]*)/(?P<resource_name>%s)/'
                '(?P<pk>[1-9][0-9]*)/$' % self._meta.resource_name,
                self.wrap_view('dispatch_detail'),
                name='api_dispatch_detail')
        ]
