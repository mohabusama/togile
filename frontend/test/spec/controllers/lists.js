'use strict';

describe('Controller: ListsCtrl', function() {

    // load the controller's module
    beforeEach(module('frontendApp'));

    var ListsCtrl, scope, api;

    // Fixtures!
    var lists = [
        {
            resource_uri: '/api/v1/users/1/lists/1',
            title: 'List 1',
            _todos: [
                {
                    value: 'Todo 1/1',
                    status: false,
                    resource_uri: '/api/v1/users/1/lists/1/todos/1'
                },
                {
                    value: 'Todo 1/2',
                    status: false,
                    resource_uri: '/api/v1/users/1/lists/1/todos/2'
                }
            ]
        },
        {
            resource_uri: '/api/v1/users/1/lists/2',
            title: 'List 2',
            _todos: []
        }
    ];

    // Initialize the controller and a mock scope
    beforeEach(inject(function($controller, $rootScope, _api_) {
        scope = $rootScope.$new();
        api = _api_;

        // Fresh copy of Lists fixture
        var _lists = angular.copy(lists);
        var _newList = {title: 'New List', resource_uri: '/api/v1/users/1/lists/3'};

        // List all
        spyOn(api.lists, 'list').andCallFake(function (loadLists) {
            loadLists(_lists);
        });

        // Create List
        spyOn(api.lists, 'create').andCallFake(function (_newList, f) {
            f(_newList);
        });

        // Update List
        spyOn(api.lists, 'update').andCallFake(function (updatedList, f) {
            f();
        });

        // Delete List
        spyOn(api.lists, 'remove').andCallFake(function (list, f) {
            f();
        });

        // Create Todo
        spyOn(api.todos, 'create').andCallFake(function (list, todo, f) {
            f(todo);
        });

        // Update Todo
        spyOn(api.todos, 'update').andCallFake(function (todo, f) {
            f(todo);
        });

        // Delete Todo
        spyOn(api.todos, 'remove').andCallFake(function (todo, f) {
            f(todo);
        });

        ListsCtrl = $controller('ListsCtrl', {
            $scope: scope,
            api: api
        });

    }));

    it('should call api.lists.list', function () {
        expect(api.lists.list).toHaveBeenCalled();
    });

    it('should have a lists object', function () {
        expect(scope.lists).toEqual(jasmine.any(Object));
        expect(scope.lists.length).toEqual(2);
        expect(scope.lists[0]._todos.length).toEqual(2);
        expect(scope.lists[1]._todos.length).toEqual(0);
    });

    it('should create a new list', function () {
        scope.createList();
        expect(api.lists.create).toHaveBeenCalled();
        expect(scope.lists.length).toEqual(3);
        expect(scope.lists[2]._todos).toEqual([]);
    });

    it('should update list with Index 1', function () {
        scope.list = scope.lists[1];
        var new_title = 'List 2 Updated!';
        scope.list.title = new_title;
        scope.updateList();
        expect(api.lists.update).toHaveBeenCalled();
        expect(scope.lists[1].title).toEqual(new_title);
        expect(scope.lists[1]._edit).toEqual(false);
    });

    it('should remove list with Index 1', function () {
        scope.list = scope.lists[0];
        scope.$index = 0;
        scope.deleteList();
        expect(api.lists.remove).toHaveBeenCalled();
        expect(scope.lists.length).toEqual(1);
        expect(scope.lists[0].title).toEqual('List 2');
    });

    it('should create a new Todo in List 2', function () {
        var list = scope.lists[1];
        list._newTodo = {value: 'Todo 2/1', resource_uri: '/api/v1/users/1/lists/2/todos/3'};
        scope.createTodo(list, 1);
        expect(api.todos.create).toHaveBeenCalled();
        expect(scope.lists[1]._todos.length).toEqual(1);
        expect(scope.lists[1]._todos[0].value).toEqual('Todo 2/1');
        expect(scope.lists[1]._newTodo.value).toEqual('');  // Test Reset
    });

    it('should update todo', function () {
        // Status
        scope.todo = scope.lists[0]._todos[0];
        scope.updateTodoStatus(true);
        expect(api.todos.update).toHaveBeenCalled();
        expect(scope.lists[0]._todos[0].status).toEqual(true);

        // Value
        scope.todo.value = 'Todo 1/1 UPDATED!';
        scope.updateTodo();
        expect(api.todos.update).toHaveBeenCalled();
        expect(scope.lists[0]._todos[0].value).toEqual('Todo 1/1 UPDATED!');
        expect(scope.lists[0]._todos[0]._edit).toEqual(false);
    });

    it('should delete first todo in list 1', function () {
        scope.todo = scope.lists[0]._todos[0];
        scope.deleteTodo(0, 0);
        expect(api.todos.remove).toHaveBeenCalled();
        expect(scope.lists[0]._todos.length).toEqual(1);
        expect(scope.lists[0]._todos[0].value).toEqual('Todo 1/2');
    });

    it('should return true when searching', function () {
        var expected = scope.lists[0]._todos[0];
        scope.needle = 'tod';
        expect(scope.comparator(expected)).toBe(true);
    });

    it('should return false when searching', function () {
        var expected = scope.lists[0]._todos[0];
        scope.needle = 'bla';
        expect(scope.comparator(expected)).toBe(false);
    });
});
