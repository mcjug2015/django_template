angular.module('template_app').controller('GlobalController', ['$scope', 'retrieveUser',
                                                               function($scope, retrieveUser) {
    "use strict";
    $scope.the_user = {'username': '', 'email': ''};
    retrieveUser($scope.the_user);
}]);