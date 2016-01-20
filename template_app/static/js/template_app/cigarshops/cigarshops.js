angular.module('template_app').controller('CigarshopsController', ['$scope', 'djangoLogin', 
                                                                   function($scope, djangoLogin) {
    $scope.username = null;
    $scope.password = null;
    $scope.django_login = function() {
        djangoLogin($scope.username, $scope.password, $scope.the_user);
    };
}]);