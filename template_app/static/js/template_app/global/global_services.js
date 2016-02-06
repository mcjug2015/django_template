angular.module('template_app').factory('retrieveUser', ['$q', 'User', function($q, User) {
    "use strict";
    var retrieveUserInstance = function(user_holder) {
        return User.get().$promise.then(function(data) {
            if (data.objects.length == 1) {
                user_holder.username = data.objects[0].username;
                user_holder.email = data.objects[0].email;
                user_holder.the_obj = data.objects[0];
            }
            return $q.when(true);
        });
    };
    return retrieveUserInstance;
}]);


angular.module('template_app').factory('djangoLogin', ['$http', '$q', 'retrieveUser',
                                                       function($http, $q, retrieveUser) {
    "use strict";
    var djangoLoginInstance = function(username, password, user_holder) {
        return $http.post('/login_async/', {'username': username, 'password': password}).then(function(data){
            if (data.data.status_code == '200') {
                retrieveUser(user_holder);
            }
            return $q.when(data);
        });
    };
    return djangoLoginInstance;
}]);
