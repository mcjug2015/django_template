angular.module('template_app').factory('User', function($resource) {
    return $resource('/api/v1/auth/user');
});