'use strict';

var togileApp = angular.module('frontendApp');


togileApp.controller('ListsCtrl', function ($scope, Restangular, api) {

    $scope.lists = [];

    // Load All Lists
    api.lists.list(loadLists);

    function loadLists(data) {
        $scope.lists = data.objects;
        _.each($scope.lists, function(list, index){
            api.todos.list(list, function(data) {
                $scope.lists[index]._todos = data.objects;
                $scope.lists[index]._newTodo = {value: '', status: false};
            });
        });
    }

    function resetList(list) {
        list._newTodo = {value: '', status: false};
    }

    $scope.deleteTodo = function(todo, todoIdx, listIdx) {
        api.todos.remove(todo,
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
        resetList(list);
    }
});
