describe("Tests for the cigarshop controller", function(){
    "use strict";
    var $controller;
    var scope = {};
    var cigarshopsController;
    var djangoLoginSpy = jasmine.createSpy('djangoLogin') ;
    beforeEach(module('template_app'));
    
    beforeEach(inject(function(_$controller_){
        $controller = _$controller_;
        cigarshopsController = $controller('CigarshopsController', {'$scope': scope,
                                                                    'djangoLogin': djangoLoginSpy});
    }));
    
    it("Goes through init and sets scope variables", function(){
        expect(scope.info_holder).toEqual({'username': '', 'password': ''});
        expect(scope.django_login).toBeDefined();
    });
    
    it("Passes username, password and user to the service method when django_login is called", function(){
        scope.django_login();
        expect(djangoLoginSpy).toHaveBeenCalledWith('', '', undefined);
    });
});