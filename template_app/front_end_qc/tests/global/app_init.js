// many thanks to https://medium.com/@a_eife/testing-config-and-run-blocks-in-angularjs-1809bd52977e#.4jua6nxek
describe("Verifies that template_app angular module got created with all the trimmings", function(){
    "use strict";
    
    describe("Make sure interpolation provider got primed", function() {
        var $interpolateProvider;

        beforeEach(function () {
            angular.module('interpolateProviderConfig', [])
                .config(function(_$interpolateProvider_) {
                    $interpolateProvider = _$interpolateProvider_;
                    spyOn($interpolateProvider, 'startSymbol');
                    spyOn($interpolateProvider, 'endSymbol');
                });
            module('interpolateProviderConfig');
            module('template_app');
            inject();
        });

        it('should set start and end symbol', function() {
            expect($interpolateProvider.startSymbol).toHaveBeenCalledWith('{[{');
            expect($interpolateProvider.endSymbol).toHaveBeenCalledWith('}]}');
        });
    });
    
    describe("make sure $httpProvider got primed", function() {
        var $httpProvider;

        beforeEach(function () {
            angular.module('httpProviderConfig', [])
                .config(function(_$httpProvider_) {
                    $httpProvider = _$httpProvider_;
                });
            module('httpProviderConfig');
            module('template_app');
            inject();
        });

        it('should set xsrfCookieName and xsrfHeaderName in defaults', function() {
            expect($httpProvider.defaults.xsrfCookieName).toEqual('csrftoken');
            expect($httpProvider.defaults.xsrfHeaderName).toEqual('X-CSRFToken');
        });
    });
});