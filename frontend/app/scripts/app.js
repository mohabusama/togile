'use strict';

var togileApp = angular.module('frontendApp',
    ['ngRoute', 'restangular', 'ngCookies']
);

// ROUTING
togileApp.config(function($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl'
    })
    .when('/lists/', {
        templateUrl: 'views/lists.html',
        controller: 'ListsCtrl'
    })
    .otherwise({
        redirectTo: '/'
    });
});

// Restangular configs
togileApp.run(function($rootScope, Restangular, $cookieStore, $cookies) {
    $rootScope.user = 1;

    Restangular.setBaseUrl('/api/v1');

    Restangular.setRequestSuffix('/');

    Restangular.setResponseExtractor(function(response, operation) {
        var apiResponse = response;
        if (operation === 'getList') {
            // Received response: { objects:[...], meta:{...} }
            // apiResponse = response.objects;
            // apiResponse._meta = response.meta
        }
        return apiResponse;
    });

    Restangular.setRestangularFields({
        selfLink: 'self.resource_uri'
    });

    //CSRF TOKEN!
    Restangular.setDefaultHeaders({
        "X-CSRFTOKEN": $cookies.csrftoken
    });
});
