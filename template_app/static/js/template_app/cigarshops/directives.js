angular.module('template_app').directive('dtCigarShop', [function() {
    "use strict";
    return {
        restrict: 'E',
        templateUrl: '/static/html/template_app/cigarshops/cigar_shop.html',
        scope: {
            shop: '=',
            editable: '='
        },
        link: function (scope, element, attrs) {
        },
    };
}]);


angular.module('template_app').directive('dtCigarShops', ['CigarShop', 'saveAndGet',
                                                          function(CigarShop, saveAndGet) {
    "use strict";
    return {
        restrict: 'E',
        templateUrl: '/static/html/template_app/cigarshops/cigar_shops.html',
        scope: {
            currentuser: '='
        },
        link: function (scope, element, attrs) {
            scope.shops = {};
            scope.shopToSave = {'name': '',
                                'location': {"lat": 0, "long": 0, "type": "Point"},
                                'owner': scope.currentuser.the_obj.resource_uri};
            scope.saveShop = function() {
                scope.shopToSave.location.coordinates = [parseFloat(scope.shopToSave.location.long),
                                                         parseFloat(scope.shopToSave.location.lat)];
                delete scope.shopToSave.location.lat;
                delete scope.shopToSave.location.long;
                saveAndGet(CigarShop.save, scope.shopToSave).then(function(newShop) {
                    scope.shops[newShop.data.id] = newShop.data;
                    scope.shopToSave = {'name': '',
                                        'location': {"lat": 0, "long": 0, "type": "Point"},
                                        'owner': scope.currentuser.the_obj.resource_uri};
                });
            };
            scope.removeShop = function(shopId) {
                CigarShop.remove({'id': shopId}).$promise.then(function() {
                    delete scope.shops[shopId];
                });
            };
            CigarShop.get().$promise.then(function(data) {
                data.objects.forEach(function(curShop) {
                    scope.shops[curShop.id] = curShop;
                });
            });
        },
    };
}]);