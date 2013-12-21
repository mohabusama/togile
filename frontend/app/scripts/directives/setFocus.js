'use strict';


togileApp.directive('setFocus', function($timeout) {
    return function(scope, element, attr) {
        scope.$watch(attr.setFocus, function(value) {
            if (value) {
                $timeout(function() {
                    element[0].focus();
                }, 0, false);
            }
        });
    };
});
