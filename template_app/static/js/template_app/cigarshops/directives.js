angular.module('template_app').directive('dtCigarShop', ['CigarShop', function(CigarShop) {
    "use strict";
    return {
        restrict: 'E',
        templateUrl: '/static/html/template_app/cigarshops/cigar_shop.html',
        scope: {
            shop: '=',
        },
        link: function (scope, element, attrs) {
            scope.startEditing = function() {
                scope.shop.beingEdited = true;
            };
            
            scope.cancelEdits = function() {
                scope.shop.beingEdited = false;
            };
            
            scope.saveEdits = function() {
                scope.shop.location.coordinates = [parseFloat(scope.shop.location.long),
                                                   parseFloat(scope.shop.location.lat)];
                CigarShop.update({id: scope.shop.id}, scope.shop).$promise.then(function() {
                    scope.shop.beingEdited = false;
                });
            };
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
                                'owner': scope.currentuser.the_obj.resource_uri,
                                'beingEdited': true,
                                'editable': false};
            scope.saveShop = function() {
                scope.shopToSave.location.coordinates = [parseFloat(scope.shopToSave.location.long),
                                                         parseFloat(scope.shopToSave.location.lat)];
                delete scope.shopToSave.location.lat;
                delete scope.shopToSave.location.long;
                saveAndGet(CigarShop.save, scope.shopToSave).then(function(newShop) {
                    var actualShop = newShop.data;
                    actualShop.beingEdited = false;
                    actualShop.editable = true;
                    actualShop.location.lat = actualShop.location.coordinates[1];
                    actualShop.location.long = actualShop.location.coordinates[0];
                    scope.shops[actualShop.id] = actualShop;
                    scope.shopToSave = {'name': '',
                                        'location': {"lat": 0, "long": 0, "type": "Point"},
                                        'owner': scope.currentuser.the_obj.resource_uri,
                                        'beingEdited': true,
                                        'editable': false};
                });
            };
            scope.removeShop = function(shopId) {
                CigarShop.remove({'id': shopId}).$promise.then(function() {
                    delete scope.shops[shopId];
                });
            };
            CigarShop.get().$promise.then(function(data) {
                data.objects.forEach(function(curShop) {
                    curShop.beingEdited = false;
                    curShop.editable = true;
                    curShop.location.lat = curShop.location.coordinates[1];
                    curShop.location.long = curShop.location.coordinates[0];
                    scope.shops[curShop.id] = curShop;
                });
            });
        },
    };
}]);