angular.module('template_app').directive('dtCigarShop', [function() {
    "use strict";
    return {
        restrict: 'E',
        templateUrl: '/static/html/template_app/cigarshops/cigar_shop.html',
        scope: {
            shop: '='
        },
        link: function (scope, element, attrs) {
        },
    };
}]);