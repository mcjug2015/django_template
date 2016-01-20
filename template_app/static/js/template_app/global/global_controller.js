angular.module('template_app').controller('GlobalController', ['$scope', function($scope) {
    $scope.logged_in = $('#global_username').text().length > 0;
    
    $scope.the_user = {'username': '', 'email': ''};
    if ($scope.logged_in) {
        $scope.the_user = {'username': $('#global_username').text(),
                           'email': $('#global_useremail').text()};
    }
    
    $scope.$watch('the_user.username', function(){
        if($scope.the_user.username.length > 0) {
            $scope.logged_in = true;
        } else {
            $scope.logged_in = false;
        }
    });
}]);