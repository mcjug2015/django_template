angular.module('template_app').factory('User', function($resource) {
    return $resource('/api/v1/auth/user');
});


angular.module('template_app').factory('CigarShop', function($resource) {
    return $resource('/api/v1/cigarshop/:id', {}, {
        'update': {method: 'PUT'},
        'partial_update': {method: 'PATCH'}
    });
});