describe("tests for the cigar shops directives", function() {
    "use strict";
    var elm;
    var $rootScope;
    var $compile;
    var parentScope;
    var dirScope;
    var $q;
    var cigarShopSpy;
    var returnedCigarShops;

    beforeEach(module("template_app"));
    beforeEach(module('test_html_js'));
    beforeEach(module(function($provide) {
        cigarShopSpy = jasmine.createSpyObj('cigarShopSpy', ['get']);
        $provide.value("CigarShop", cigarShopSpy);
    }));
    
    beforeEach(inject(function(_$rootScope_, _$compile_, _$q_) {
        $rootScope = _$rootScope_;
        $compile = _$compile_;
        $q = _$q_;
        parentScope = $rootScope.$new();
    }));
    
    describe("tests for the cigar shop directive", function() {
        beforeEach(function() {
            elm = angular.element("<dt-cigar-shop shop='theShop'></dt-cigar-shop>");
        });
        
        it("fills out the dtCigarShop template with shop info", function() {
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
    });
    
    describe("tests for the cigar shops directive", function() {
        beforeEach(function() {
            returnedCigarShops = [];
            elm = angular.element("<dt-cigar-shops></dt-cigar-shops>");
            cigarShopSpy.get.and.returnValue({'$promise': $q.when({'objects': returnedCigarShops})});
        });
        
        it("fills out the dtCigarShops template when no cigar shops are returned", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('span').text()).toEqual('Here are your cigar shops:');
            expect(elm.find('dt-cigar-shop').size()).toEqual(0);
        });
        
        it("fills out the dtCigarShops template when cigar shops are returned", function() {
            returnedCigarShops.push({'id': 'a',
                                     'name': 'Test shop for directive',
                                     'owner': '/api/v1/auth/user/1/',
                                     "location": {"coordinates": [-75.130205, 37.067922], "type": "Point"}});
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('span').text()).toEqual('Here are your cigar shops:');
            expect(elm.find('dt-cigar-shop').size()).toEqual(1);
        });
    });
});