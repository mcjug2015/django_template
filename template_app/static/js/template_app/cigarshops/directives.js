angular.module('template_app').directive('dtCigarShop', ['CigarShop', 'getServerShop',
                                                         'copyClientShop',
                                                         function(CigarShop, getServerShop,
                                                                  copyClientShop) {
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
                scope.initial_shop = {};
                copyClientShop(scope.initial_shop, scope.shop);
            };
            
            scope.cancelEdits = function() {
                copyClientShop(scope.shop, scope.initial_shop);
                scope.shop.beingEdited = false;
            };
            
            scope.saveEdits = function() {
                CigarShop.update({id: scope.shop.id}, getServerShop(scope.shop)).$promise.then(function() {
                    scope.shop.beingEdited = false;
                });
            };
        },
    };
}]);


angular.module('template_app').directive('dtCigarShops', ['CigarShop', 'saveAndGet', 'getServerShop',
                                                          'getClientShop',
                                                          function(CigarShop, saveAndGet, getServerShop,
                                                                   getClientShop) {
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
                                'location': {"lat": 0, "long": 0},
                                'owner': scope.currentuser.the_obj.resource_uri,
                                'beingEdited': true,
                                'editable': false};
            scope.saveShop = function() {
                saveAndGet(CigarShop.save, getServerShop(scope.shopToSave)).then(function(newShop) {
                    var actualShop = getClientShop(newShop.data);
                    scope.shops[actualShop.id] = actualShop;
                    scope.shopToSave = {'name': '',
                                        'location': {"lat": 0, "long": 0},
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
                    var clientShop = getClientShop(curShop);
                    scope.shops[clientShop.id] = clientShop;
                });
            });
        },
    };
}]);