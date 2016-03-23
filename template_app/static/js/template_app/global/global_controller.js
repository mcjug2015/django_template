angular.module('template_app').controller('GlobalController', ['$scope', 'retrieveUser',
                                                               function($scope, retrieveUser) {
    "use strict";
    $scope.theUser = {'username': '', 'email': ''};
    retrieveUser($scope.theUser);
}]);