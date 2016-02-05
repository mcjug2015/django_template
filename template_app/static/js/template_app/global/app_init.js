angular.module('template_app', ['ngCookies']).config(function($interpolateProvider){
    // not gonna be using django templates a lot, but don't want them to collide either.
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}).config(['$httpProvider', function($httpProvider){
    // django and angular both support csrf tokens. This tells
    // angular which cookie to add to what header.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);