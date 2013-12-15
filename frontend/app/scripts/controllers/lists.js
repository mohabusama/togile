'use strict';

var togileApp = angular.module('frontendApp');


togileApp.controller('ListsCtrl', function ($scope, Restangular, api) {

    // Load All Lists
    api.lists.list(loadLists);
    $scope.lists = [];

    function loadLists(data) {
        $scope.lists = data.objects;
        _.each($scope.lists, function(list, index){
            api.todos.list(list, function(data) {
                $scope.lists[index]._todos = data.objects;
            });
        });
    }
});
