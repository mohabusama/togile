'use strict';

var togileApp = angular.module('frontendApp');

togileApp.factory('api', function($rootScope, Restangular) {
    var api = Restangular.one('users', $rootScope.user);

    function _getListsApi(id) {
        return (id) ? api.one('lists', id) : api.all('lists');
    }

    function _getTodosApi(list, todo) {
        var uri = (list) ? list.resource_uri.replace(/\/$/, '') : '';
        return (todo) ?
            api.oneUrl('todos', todo.resource_uri) :
            api.oneUrl('lists', uri).all('todos');
    }

    // LISTS APIs
    function listsList(callback, errCallback) {
        var _api = _getListsApi();
        _api.getList()
            .then(callback, errCallback);
    }

    function listsGet(list, callback, errCallback) {
        list.get()
            .then(callback, errCallback);
    }

    function listsCreate(data, callback, errCallback) {
        var _api = _getListsApi();
        _api.post(data)
            .then(callback, errCallback);
    }

    function listsUpdate(list, data, callback, errCallback) {
        list.put(data)
            .then(callback, errCallback);
    }

    function listsRemove(list, callback, errCallback) {
        list.remove()
            .then(callback, errCallback);
    }

    // TODOS APIs
    function todosList(list, callback, errCallback) {
        var _api = _getTodosApi(list);
        _api.getList()
            .then(callback, errCallback);
    }

    function todosGet(todo, callback, errCallback) {
        var _api = _getTodosApi(null, todo);
        _api.get()
            .then(callback, errCallback);
    }

    function todosCreate(list, data, callback, errCallback) {
        var _api = _getTodosApi(list);
        _api.post(data)
            .then(callback, errCallback);
    }

    function todosUpdate(todo, data, callback, errCallback) {
        var _api = _getTodosApi(null, todo);
        _api.put(data)
            .then(callback, errCallback);
    }

    function todosRemove(todo, callback, errCallback) {
        var _api = _getTodosApi(null, todo);
        _api.remove()
            .then(callback, errCallback);
    }

    return {
        lists: {
            list: listsList,
            get: listsGet,
            create: listsCreate,
            update: listsUpdate,
            remove: listsRemove
        },
        todos: {
            list: todosList,
            get: todosGet,
            create: todosCreate,
            update: todosUpdate,
            remove: todosRemove
        }
    };
});
