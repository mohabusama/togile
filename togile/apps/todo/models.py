from django.db import models
from django.contrib.auth.models import User


class TodoList(models.Model):
    user = models.ForeignKey(User)
    parent = models.ForeignKey('TodoItem', unique=True, null=True,
                               blank=True, related_name='parent_todo',
                               help_text='Parent Todo Item')
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.title


class TodoItem(models.Model):
    todo_list = models.ForeignKey(TodoList, related_name='todo_list')
    value = models.TextField()
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.value
