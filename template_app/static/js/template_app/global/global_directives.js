angular.module('template_app').directive('dtUserCpHeader', ['djangoLogin', 'djangoLogout',
                                                            function(djangoLogin, djangoLogout) {
    "use strict";
    return {
        restrict: 'E',
        templateUrl: '/static/html/template_app/global/user_cp_header.html',
        scope: {
            diruser: '='
        },
        link: function (scope, element, attrs) {
            scope.info_holder = {'username': '', 'password': ''};
            scope.django_login = function() {
                djangoLogin(scope.info_holder.username, scope.info_holder.password, scope.diruser);
            };
            scope.django_logout = function() {
                djangoLogout(scope.diruser);
            };
        },
    };
}]);