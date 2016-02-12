describe("tests for the global directives", function() {
    "use strict";
    beforeEach(module("template_app"));
    beforeEach(module('test_html_js'));
    var elm;
    var $rootScope;
    
    describe("tests for the user control panel header directive", function() {
        beforeEach(inject(function(_$rootScope_, $compile) {
            elm = angular.element("<dt-user-cp-header></dt-user-cp-header>");
            $rootScope = _$rootScope_;
            $compile(elm)($rootScope);
            $rootScope.$digest();
        }));
        
        it("fills out the dtUserCpHeader template", function() {
            expect(elm.find('div').text()).toEqual('MOOOOO!');
        });
    });
});