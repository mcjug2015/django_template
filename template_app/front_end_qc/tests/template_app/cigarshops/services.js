describe("Tests for the cigarshop services", function() {
    "use strict";
    beforeEach(module("template_app"));
    var $rootScope;
    var retval;
    
    
    describe("tests for the getClientShopService", function() {
        var getClientShopService;
        
        beforeEach(inject(function(_$rootScope_, getClientShop) {
            $rootScope = _$rootScope_;
            getClientShopService = getClientShop;
        }));
        
        it("converts a server format shop into a client format shop", function() {
            var serverShop = {'name': 'a',
                              'id': 'b',
                              'owner': 'c',
                              'resource_uri': 'd',
                              'location': {'coordinates': ['e', 'f']}};
            retval = getClientShopService(serverShop);
            expect(retval).toEqual({'name': 'a', 
                                    'location': {'lat': 'f', 'long': 'e'}, 
                                    'id': 'b',
                                    'resource_uri': 'd',
                                    'owner': 'c',
                                    'beingEdited': false,
                                    'editable': true});
        });
    });
    
    
    describe("tests for the getServerShopService", function() {
        var getServerShopService;
        
        beforeEach(inject(function(_$rootScope_, getServerShop) {
            $rootScope = _$rootScope_;
            getServerShopService = getServerShop;
        }));
        
        it("converts a client format shop into a server format shop", function() {
            var serverShop = {'name': 'a',
                              'id': 'b',
                              'owner': 'c',
                              'resource_uri': 'd',
                              'location': {'lat': 1, 'long': 2}};
            retval = getServerShopService(serverShop);
            expect(retval).toEqual({'name': 'a',
                                    'location': {coordinates: [2, 1], type: 'Point'},
                                    'id': 'b',
                                    'resource_uri': 'd',
                                    'owner': 'c'});
        });
    });


    describe("tests for the copyClientShop Service", function() {
        var copyClientShopService;
        
        beforeEach(inject(function(_$rootScope_, copyClientShop) {
            $rootScope = _$rootScope_;
            copyClientShopService = copyClientShop;
        }));
        
        it("converts a client format shop into a server format shop", function() {
            var toShop = {'name': 'a',
                          'id': 'b',
                          'owner': 'c',
                          'resource_uri': 'd',
                          'location': {'lat': 1, 'long': 2},
                          'beingEdited': 'e',
                          'editable': 'f'};
            var fromShop = {'name': 'a1',
                            'id': 'b1',
                            'owner': 'c1',
                            'resource_uri': 'd1',
                            'location': {'lat': 99, 'long': 100},
                            'beingEdited': 'e1',
                            'editable': 'f1'};
            retval = copyClientShopService(toShop, fromShop);
            expect(toShop).toEqual({'name': 'a1',
                                    'id': 'b1',
                                    'owner': 'c1',
                                    'resource_uri': 'd1',
                                    'location': {'lat': 99, 'long': 100},
                                    'beingEdited': 'e1',
                                    'editable': 'f1'});
        });
    });
});