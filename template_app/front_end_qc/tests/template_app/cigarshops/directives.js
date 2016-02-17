describe("tests for the cigar shops directives", function() {
    "use strict";
    beforeEach(module("template_app"));
    beforeEach(module('test_html_js'));
    var elm;
    var $rootScope;
    var $compile;
    var parentScope;
    var dirScope;
    
    describe("tests for the cigar shop directive", function() {
        
        beforeEach(inject(function(_$rootScope_, _$compile_) {
            elm = angular.element("<dt-cigar-shop shop='theShop'></dt-cigar-shop>");
            $rootScope = _$rootScope_;
            $compile = _$compile_;
            parentScope = $rootScope.$new();
        }));
        
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
});