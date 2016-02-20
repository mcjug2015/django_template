angular.module('template_app').factory('retrieveUser', ['$q', 'User', function($q, User) {
    "use strict";
    var retrieveUserInstance = function(user_holder) {
        return User.get().$promise.then(function(data) {
            if (data.objects.length == 1) {
                user_holder.username = data.objects[0].username;
                user_holder.email = data.objects[0].email;
                user_holder.the_obj = data.objects[0];
            } else {
                user_holder.username = '';
                user_holder.email = '';
                user_holder.the_obj = null;
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


angular.module('template_app').factory('djangoLogout', ['$http', '$q', 'retrieveUser',
                                                       function($http, $q, retrieveUser) {
    "use strict";
    var djangoLogoutInstance = function(user_holder) {
        return $http.get('/logout_async/').then(function(data){
            retrieveUser(user_holder);
            return $q.when(true);
        });
    };
    return djangoLogoutInstance;
}]);


angular.module('template_app').factory('saveAndGet', ['$q', '$http',
                                                      function($q, $http) {
    // calls the provided save method with the supplied params.
    // expects a location header to be returned. does a get on that location header
    // and returns the object that was retrieved.
    "use strict";
    var saveAndGetInstance = function(saveMethod, methodParams) {
        return saveMethod(methodParams, function(data, headers) {
            return $http.get(headers('location'));
        }).$promise;
    };
    return saveAndGetInstance;
}]);