describe("Tests for the global controller", function() {
    "use strict";
    beforeEach(module('template_app'));
    var $controller;
    var scope = {};
    var globalController;
    var retrieveUserSpy = jasmine.createSpy('retrieveUser');
    
    beforeEach(inject(function(_$controller_) {
        $controller = _$controller_;
        globalController = $controller('GlobalController', {'$scope': scope,
                                                            'retrieveUser': retrieveUserSpy});
    }));
    
    it("inits the_user obj and calls retrieve user", function() {
        expect(scope.theUser).toEqual({'username': '', 'email': ''});
        expect(retrieveUserSpy).toHaveBeenCalledWith(scope.theUser);
    });
});