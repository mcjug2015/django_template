angular.module('template_app', ['ngCookies']).config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[{').endSymbol('}]}');
}).config(['$httpProvider', '$cookiesProvider', function($httpProvider, $cookiesProvider){
    // django and angular both support csrf tokens. This tells
    // angular which cookie to add to what header.
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['X-CSRFToken'] = $cookiesProvider.csrftoken;
    $httpProvider.defaults.headers.put['X-CSRFToken'] = $cookiesProvider.csrftoken;
    $httpProvider.defaults.headers.patch['X-CSRFToken'] = $cookiesProvider.csrftoken;
    $httpProvider.defaults.headers['delete'] = {'X-CSRFToken': $cookiesProvider.csrftoken};
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $cookiesProvider.csrftoken;
}]);