'use strict';

var togileApp = angular.module('frontendApp');


togileApp.controller('ListsCtrl', function ($scope, Restangular, api) {

    $scope.lists = [];
    $scope._newList = {title: ''};

    // Load All Lists
    api.lists.list(loadLists);

    function loadLists(data) {
        $scope.lists = data;
        _.each($scope.lists, function(list, index){
            api.todos.list(list, function(data) {
                $scope.lists[index]._todos = data;
                $scope.lists[index]._newTodo = {value: '', status: false};
            });
        });
    }

    function resetList() {
        $scope._newList = {title: ''};
    }

    function resetTodo(list) {
        list._newTodo = {value: '', status: false};
    }

    // LISTS OPERATONS
    $scope.createList = function(todo) {
        api.lists.create(this._newList,
            function(newList) {
                newList._todos = [];
                resetTodo(newList); // actually, initializing!
                $scope.lists.push(newList);
            },
            function() {

            }
        );
        resetList();
    }

    $scope.updateList = function() {
        var _this = this;
        api.lists.update(this.list,
            function(data) {
                _this.list._edit = false;
            },
            function() {

            }
        );
    }

    $scope.deleteList = function() {
        var _this = this;
        api.lists.remove(this.list,
            function(data) {
                $scope.lists.splice(_this.$index, 1);
            },
            function() {

            }
        );
    }

    // TODO OPERATIONS
    $scope.deleteTodo = function(todo, todoIdx, listIdx) {
        api.todos.remove(this.todo,
            function(){
                // success
                $scope.lists[listIdx]._todos.splice(todoIdx, 1);
            },
            function(){
                // ERROR!
            }
        );
    }

    $scope.createTodo = function(list, listIdx) {
        if (!list._newTodo.value) {
            return;
        }
        api.todos.create(list, list._newTodo,
            function(todo) {
                $scope.lists[listIdx]._todos.push(todo);
            },
            function() {
                // ERROR!
            }
        );
        resetTodo(list);
    }

    $scope.updateTodoStatus = function(status) {
        var _this = this;
        this.todo.status = status;
        api.todos.update(this.todo,
            function(data) {
                _this.todo.status = data.status;
            },
            function() {
                // ERROR!
            }
        );
    }

    $scope.updateTodo = function() {
        var _this = this;
        api.todos.update(this.todo,
            function(data) {
                _this.todo._edit = false;
            },
            function() {
                // ERROR!
            }
        );
    }

    // SEARCH
    $scope.comparator = function (expected) {
        // TODO: Fuzzy search!
        var val = expected.value.toLowerCase(),
            needle = $scope.needle;
        if(needle && val.indexOf(needle.toLowerCase()) != -1) {
            return true;
        }
        return false;
    }
});

