describe("tests for the cigar shops directives", function() {
    "use strict";
    var elm;
    var $rootScope;
    var $compile;
    var parentScope;
    var dirScope;
    var $q;
    var cigarShopSpy;
    var saveAndGetSpy;
    var returnedCigarShops;
    

    beforeEach(module("template_app"));
    beforeEach(module('test_html_js'));
    beforeEach(module(function($provide) {
        cigarShopSpy = jasmine.createSpyObj('cigarShopSpy', ['get']);
        $provide.value("CigarShop", cigarShopSpy);

        saveAndGetSpy = jasmine.createSpy('saveAndGet');
        $provide.value("saveAndGet", saveAndGetSpy);
    }));
    
    beforeEach(inject(function(_$rootScope_, _$compile_, _$q_) {
        $rootScope = _$rootScope_;
        $compile = _$compile_;
        $q = _$q_;
        parentScope = $rootScope.$new();
    }));
    
    describe("tests for the cigar shop directive", function() {
        beforeEach(function() {
            elm = angular.element("<dt-cigar-shop shop='theShop' editable='modify'></dt-cigar-shop>");
        });
        
        it("fills out the dtCigarShop template with shop info", function() {
            parentScope.modify = false;
            parentScope.theShop = {'name': 'Test shop for directive',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"coordinates": [-75.130205, 37.067922], "type": "Point"}};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('div div').first().text()).toEqual('Test shop for directive');
            expect(elm.find('div div div').first().text()).toEqual('37.067922');
            expect(elm.find('div div div').last().text()).toEqual('-75.130205');
            expect(dirScope.shop).toBeDefined();
            expect(dirScope.shop.name).toEqual('Test shop for directive');
        });
        
        it("fills out the dtCigarShop template with editable shop info", function() {
            parentScope.modify = true;
            parentScope.theShop = {'name': 'Test editable shop',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"lat": 1.3, "long": 6.8}};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(dirScope.shop).toBeDefined();
            expect(dirScope.shop.name).toEqual('Test editable shop');
            expect(dirScope.editable).toEqual(true);
            expect(elm.find('div input').first().val()).toEqual('Test editable shop');
            expect(elm.find('div div input').first().val()).toEqual('1.3');
            expect(elm.find('div div input').last().val()).toEqual('6.8');
        });
    });
    
    describe("tests for the cigar shops directive", function() {
        var saveAndGetResults;
        
        beforeEach(function() {
            returnedCigarShops = [];
            elm = angular.element('<dt-cigar-shops currentuser="theUser"></dt-cigar-shops>');
            cigarShopSpy.get.and.returnValue({'$promise': $q.when({'objects': returnedCigarShops})});
            parentScope.theUser = {'the_obj': {'resource_uri': 'test_owner_uri'}};
            
            saveAndGetResults = {};
            saveAndGetSpy.and.returnValue($q.when(saveAndGetResults));
        });
        
        it("fills out the dtCigarShops template when no cigar shops are returned", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('span').first().text()).toEqual('Create a new cigarshop:');
            expect(elm.find('span').last().text()).toEqual('Here are your existing cigar shops:');
            expect(elm.find('dt-cigar-shop').size()).toEqual(1);
            expect(dirScope.shopToSave.location.lat).toEqual(0);
            expect(dirScope.shopToSave.owner).toEqual('test_owner_uri');
            expect(dirScope.saveShop).toBeDefined();
        });
        
        it("fills out the dtCigarShops template when cigar shops are returned", function() {
            returnedCigarShops.push({'id': 'a',
                                     'name': 'Test shop for directive',
                                     'owner': '/api/v1/auth/user/1/',
                                     "location": {"coordinates": [-75.130205, 37.067922], "type": "Point"}});
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('span').first().text()).toEqual('Create a new cigarshop:');
            expect(elm.find('span').last().text()).toEqual('Here are your existing cigar shops:');
            expect(elm.find('dt-cigar-shop').size()).toEqual(2);
        });
        
        it("invokes the saveShop method and updates on success", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('dt-cigar-shop').size()).toEqual(1);
            
            saveAndGetResults.id = 'testid';
            saveAndGetResults.name = 'freshly saved shop';
            saveAndGetResults.location = {"coordinates": [-75.111111, 37.222222], "type": "Point"};
            dirScope.shopToSave.name = 'i will get reset';
            dirScope.saveShop();
            parentScope.$digest();
            expect(elm.find('dt-cigar-shop').size()).toEqual(2);
            expect(elm.find('dt-cigar-shop').last().find('div div').first().text()).toEqual('freshly saved shop');
            expect(dirScope.shopToSave.name).toEqual('');
        });
    });
});