from django.contrib import admin

from togile.apps.todo.models import TodoItem, TodoList


class TodoListAdmin(admin.ModelAdmin):
    list_display = ('title', 'user',)


class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('value', 'todo_list',)


admin.site.register(TodoList, TodoListAdmin)
admin.site.register(TodoItem, TodoItemAdmin)
