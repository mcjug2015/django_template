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
    
    describe("Tests for the user resource", function() {
        beforeEach(inject(function (CigarShop) {
            resourceUnderTest = CigarShop;
        }));
        
        it("sends proper get params for cigarshop get request", function() {
            var getAppendix = "?distance=10&lat=37.067922&long=-75.130205";
            httpBackend.expectGET('/api/v1/cigarshop' + getAppendix).respond(200, {'objects': ['a', 'b']});
            retval = resourceUnderTest.get({'lat': 37.067922,
                                            'long': -75.130205,
                                            'distance': 10});
            httpBackend.flush();
            expect(retval.objects[1]).toEqual('b');
        });
        
        it("sends proper get params for cigarshop list get request", function() {
            var getAppendix = "?distance=10&lat=37.067922&long=-75.130205";
            httpBackend.expectGET('/api/v1/cigarshop' + getAppendix).respond(200, {'objects': ['a', 'b']});
            retval = resourceUnderTest.get({'lat': 37.067922,
                                            'long': -75.130205,
                                            'distance': 10});
            httpBackend.flush();
            expect(retval.objects[1]).toEqual('b');
        });
        
        it("sends proper params for cigarshop save/post request", function() {
            var cigarShopObj = {'name': 'brand new cigar shop',
                                'owner': '/api/v1/auth/user/1/',
                                "location": {"coordinates": [-77.0, 39.0], "type": "Point"}};
            
            httpBackend.expectPOST('/api/v1/cigarshop', cigarShopObj).respond(201, {'it': 'worked'});
            retval = resourceUnderTest.save(cigarShopObj);
            httpBackend.flush();
            expect(retval.it).toEqual('worked');
        });
        
        it("sends proper params for cigarshop update/put request", function() {
            var cigarShopObj = {'id': 1,
                                'name': 'brand new cigar shop(updated)',
                                'owner': '/api/v1/auth/user/1/',
                                "location": {"coordinates": [-77.0, 39.0], "type": "Point"}};

            httpBackend.expectPUT('/api/v1/cigarshop/1', cigarShopObj).respond(204, {'it': 'worked again'});
            retval = resourceUnderTest.update({id: 1}, cigarShopObj);
            httpBackend.flush();
            expect(retval.it).toEqual('worked again');
        });
        
        it("sends proper params for cigarshop partial_update/path request", function() {
            var cigarShopObj = {'name': 'brand new cigar shop(patched)'};
            httpBackend.expectPATCH('/api/v1/cigarshop/1', cigarShopObj).respond(202, {'it': 'patched'});
            retval = resourceUnderTest.partial_update({id: 1}, cigarShopObj);
            httpBackend.flush();
            expect(retval.it).toEqual('patched');
        });
        
        it("sends proper params for cigarshop remove/delete request", function() {
            httpBackend.expectDELETE('/api/v1/cigarshop/1').respond(204, {'it': 'deleted'});
            retval = resourceUnderTest.remove({id: 1});
            httpBackend.flush();
            expect(retval.it).toEqual('deleted');
        });
    });
});