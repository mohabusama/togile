from tastypie.api import Api
from togile.apps.todo.resources import TodoListResource, TodoItemResource


togile_api = Api(api_name='v1')

togile_api.register(TodoListResource())
togile_api.register(TodoItemResource())
