'use strict';

var togileApp = angular.module('frontendApp');

togileApp.directive('keyEnter', function() {

    return function (scope, element, attr) {
        element.bind("keypress", function(event) {
            if(event.keyCode === 13) {
                scope.$apply(function() {
                    scope.$eval(attr.keyEnter);
                });
                event.preventDefault();
            }
        });
    }
});