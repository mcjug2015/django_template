angular.module('template_app').factory('djangoLogin', [function() {
    var djangoLoginInstance = function(username, password, user_holder) {
        user_holder.username = 'test';
        user_holder.email = 'test@test.com';
    };
    return djangoLoginInstance;
}]);