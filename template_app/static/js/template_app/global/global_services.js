angular.module('template_app').factory('djangoLogin', ['$http', '$q', function($http, $q) {
    "use strict";
    var djangoLoginInstance = function(username, password, user_holder) {
        return $http.post('/login_async/', {'username': username, 'password': password}).then(function(data){
            if (data.data.status_code == '200') {
                user_holder.username = username;
                user_holder.email = 'coming soon@test.com';
            }
            return $q.when(data);
        });
    };
    return djangoLoginInstance;
}]);