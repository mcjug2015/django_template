describe("Tests for the global resources", function() {
    "use strict";
    beforeEach(module("template_app"));
    var resourceUnderTest;
    var httpBackend;
    var retval;
    
    beforeEach(inject(function ($httpBackend) {
        httpBackend = $httpBackend;
    }));
    
    describe("Tests for the user resource", function() {
        beforeEach(inject(function (User) {
            resourceUnderTest = User;
            httpBackend.expectGET('/api/v1/auth/user').respond(200, {'username': 'testing...'});
        }));
        
        it("calls user endpoint and returns users", function() {
            retval = resourceUnderTest.get();
            httpBackend.flush();
            expect(retval.username).toEqual('testing...');
        });
    });
});