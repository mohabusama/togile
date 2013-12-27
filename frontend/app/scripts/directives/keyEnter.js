'use strict';

/*globals togileApp*/

togileApp.directive('keyEnter', function () {
    return function (scope, element, attr) {
        element.bind('keypress', function(event) {
            if (event.keyCode === 13) {
                scope.$apply(function () {
                    scope.$eval(attr.keyEnter);
                });
                event.preventDefault();
            }
        });
    };
}).directive('keyEsc', function () {
    return function (scope, element, attr) {
        element.bind('keyup keypress', function(event) {
            if (event.keyCode === 27) {
                scope.$apply(function () {
                    scope.$eval(attr.keyEsc);
                });
                event.preventDefault();
            }
        });
    };
});
