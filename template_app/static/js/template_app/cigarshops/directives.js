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


angular.module('template_app').directive('dtCigarShops', ['CigarShop', function(CigarShop) {
    "use strict";
    return {
        restrict: 'E',
        templateUrl: '/static/html/template_app/cigarshops/cigar_shops.html',
        scope: {
        },
        link: function (scope, element, attrs) {
            scope.shops = {};
            CigarShop.get().$promise.then(function(data) {
                data.objects.forEach(function(curShop) {
                    scope.shops[curShop.id] = curShop;
                });
            });
        },
    };
}]);