angular.module('template_app').controller('CigarshopsController', ['$scope', 'djangoLogin', 
                                                                   function($scope, djangoLogin) {
    "use strict";
    $scope.info_holder = {};
    $scope.info_holder.username = '';
    $scope.info_holder.password = '';
    $scope.django_login = function() {
        djangoLogin($scope.info_holder.username, $scope.info_holder.password, $scope.the_user);
    };
}]);