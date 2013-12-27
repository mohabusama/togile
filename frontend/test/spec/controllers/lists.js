'use strict';

describe('Controller: ListsCtrl', function() {

    // load the controller's module
    beforeEach(module('frontendApp'));

    var ListsCtrl, scope;

    // Initialize the controller and a mock scope
    beforeEach(inject(function($controller, $rootScope) {
        scope = $rootScope.$new();
        ListsCtrl = $controller('ListsCtrl', {
            $scope: scope
        });
    }));

    it('should have a lists object', function() {
        expect(scope.lists).toEqual(jasmine.any(Object));
    });
});
