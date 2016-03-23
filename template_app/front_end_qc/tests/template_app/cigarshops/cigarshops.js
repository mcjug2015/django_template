describe("Tests for the cigarshop controller", function(){
    "use strict";
    var $controller;
    var scope = {};
    var cigarshopsController;
    beforeEach(module('template_app'));
    
    beforeEach(inject(function(_$controller_){
        $controller = _$controller_;
        cigarshopsController = $controller('CigarshopsController', {'$scope': scope});
    }));
    
    it("inits cigarshop controller", function() {
        // noop for now.
        expect(scope).toBeDefined();
    });
});