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
    var getServerShopSpy;
    var getClientShopSpy;
    var returnedCigarShops;

    beforeEach(module("template_app"));
    beforeEach(module('test_html_js'));
    beforeEach(module(function($provide) {
        cigarShopSpy = jasmine.createSpyObj('cigarShopSpy', ['get', 'remove', 'update']);
        $provide.value("CigarShop", cigarShopSpy);

        saveAndGetSpy = jasmine.createSpy('saveAndGet');
        $provide.value("saveAndGet", saveAndGetSpy);
        
        getServerShopSpy = jasmine.createSpy('getServerShop');
        $provide.value("getServerShop", getServerShopSpy);
        
        getClientShopSpy = jasmine.createSpy('getClientShop');
        $provide.value("getClientShop", getClientShopSpy);
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
            cigarShopSpy.update.and.returnValue({'$promise': $q.when(true)});
        });
        
        it("fills out the dtCigarShop template with shop info", function() {
            parentScope.theShop = {'name': 'Test shop for directive',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"lat": 37.067922, "long": -75.130205},
                                   'beingEdited': false,
                                   'editable': true};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('div div').first().text()).toEqual('Test shop for directive');
            expect(elm.find('div div div').first().text()).toEqual('37.067922');
            expect(elm.find('div div div').last().text()).toEqual('-75.130205');
            expect(elm.find('div button').text()).toEqual('Update');
            expect(dirScope.shop).toBeDefined();
            expect(dirScope.shop.name).toEqual('Test shop for directive');
        });
        
        it("fills out the dtCigarShop template with editable shop info", function() {
            parentScope.theShop = {'name': 'Test editable shop',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"lat": 1.3, "long": 6.8},
                                   'beingEdited': true,
                                   'editable': true};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(dirScope.shop).toBeDefined();
            expect(dirScope.shop.name).toEqual('Test editable shop');
            expect(elm.find('div input').first().val()).toEqual('Test editable shop');
            expect(elm.find('div div input').first().val()).toEqual('1.3');
            expect(elm.find('div div input').last().val()).toEqual('6.8');
            expect(elm.find('div button').first().text()).toEqual('Save Update');
            expect(elm.find('div button').last().text()).toEqual('Cancel Update');
        });
        
        it("shows editable fields when startEditing is called", function() {
            parentScope.theShop = {'name': 'Test editable shop to be',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"lat": 1.3, "long": 6.8},
                                   'beingEdited': false,
                                   'editable': true};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            dirScope.startEditing();
            expect(dirScope.shop.beingEdited).toEqual(true);
            parentScope.$digest();
            expect(elm.find('div input').first().val()).toEqual('Test editable shop to be');
            expect(elm.find('div div input').first().val()).toEqual('1.3');
            expect(elm.find('div div input').last().val()).toEqual('6.8');
            expect(elm.find('div button').first().text()).toEqual('Save Update');
            expect(elm.find('div button').last().text()).toEqual('Cancel Update');
        });
        
        it("hides editable fields when cancelEdits is called", function() {
            parentScope.theShop = {'name': 'Test shop',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"lat": 1.3, "long": 6.8},
                                   'beingEdited': true,
                                   'editable': true};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            dirScope.cancelEdits();
            expect(dirScope.shop.beingEdited).toEqual(false);
            parentScope.$digest();
            expect(elm.find('div div').first().text()).toEqual('Test shop');
            expect(elm.find('div div div').first().text()).toEqual('1.300000');
            expect(elm.find('div div div').last().text()).toEqual('6.800000');
            expect(elm.find('div button').text()).toEqual('Update');
            expect(dirScope.shop).toBeDefined();
            expect(dirScope.shop.name).toEqual('Test shop');
        });
        
        it("invokes update and stops editing when saveEdits is called", function() {
            parentScope.theShop = {'id': 3,
                                   'name': 'Test shop',
                                   'owner': '/api/v1/auth/user/1/',
                                   "location": {"lat": 1.11, "long": 7.77},
                                   'beingEdited': true,
                                   'editable': true};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            dirScope.saveEdits();
            
            expect(getServerShopSpy).toHaveBeenCalled();
            parentScope.$digest();
            expect(dirScope.shop.beingEdited).toEqual(false);
            expect(elm.find('div div').first().text()).toEqual('Test shop');
            expect(elm.find('div div div').first().text()).toEqual('1.110000');
            expect(elm.find('div div div').last().text()).toEqual('7.770000');
            expect(elm.find('div button').text()).toEqual('Update');
        });
    });
    
    describe("tests for the cigar shops directive", function() {
        var saveAndGetResults;
        
        beforeEach(function() {
            returnedCigarShops = [];
            elm = angular.element('<dt-cigar-shops currentuser="theUser"></dt-cigar-shops>');
            cigarShopSpy.get.and.returnValue({'$promise': $q.when({'objects': returnedCigarShops})});
            cigarShopSpy.remove.and.returnValue({'$promise': $q.when(true)});
            parentScope.theUser = {'the_obj': {'resource_uri': 'test_owner_uri'}};
            
            saveAndGetResults = {};
            saveAndGetSpy.and.returnValue($q.when(saveAndGetResults));
            
            getClientShopSpy.and.returnValue({'name': 'shop converted to client format',
                                              'location': {'lat': 1, 'long': 2},
                                              'id': 'test_id',
                                              'owner': 'test_owner',
                                              'resource_uri': 'test_resource_uri',
                                              'editable': true,
                                              'beingEdited': false});
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
            returnedCigarShops.push({'I': 'will be converted to a client format shop'});
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            
            expect(cigarShopSpy.get).toHaveBeenCalled();
            expect(getClientShopSpy).toHaveBeenCalledWith({'I': 'will be converted to a client format shop'});
            expect(elm.find('span').first().text()).toEqual('Create a new cigarshop:');
            expect(elm.find('span').last().text()).toEqual('Here are your existing cigar shops:');
            expect(elm.find('div div button').last().text()).toEqual('Delete');
            expect(elm.find('dt-cigar-shop').size()).toEqual(2);
            expect(elm.find('dt-cigar-shop').last().find('button').text()).toEqual('Update');
            expect(dirScope.shops.test_id.beingEdited).toEqual(false);
            expect(dirScope.shops.test_id.editable).toEqual(true);
            expect(dirScope.shops.test_id.location.lat).toEqual(1);
            expect(dirScope.shops.test_id.location.long).toEqual(2);
        });
        
        it("invokes the saveShop method and updates on success", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('dt-cigar-shop').size()).toEqual(1);
            
            saveAndGetResults.data = {'I': 'will be converted to client format shop'};
            dirScope.shopToSave.name = 'i will get reset';
            dirScope.saveShop();
            expect(getServerShopSpy).toHaveBeenCalled();
            
            parentScope.$digest();
            expect(getClientShopSpy).toHaveBeenCalledWith({'I': 'will be converted to client format shop'});
            expect(elm.find('dt-cigar-shop').size()).toEqual(2);
            expect(elm.find('dt-cigar-shop').last().find('div div').first().text()).toEqual('shop converted to client format');
            expect(dirScope.shopToSave.name).toEqual('');
            expect(dirScope.shops.test_id.name).toEqual('shop converted to client format');
            expect(dirScope.shops.test_id.beingEdited).toEqual(false);
            expect(dirScope.shops.test_id.editable).toEqual(true);
            expect(dirScope.shops.test_id.location.lat).toEqual(1);
            expect(dirScope.shops.test_id.location.long).toEqual(2);
        });
        
        it("invokes the removeShop method and updates on success", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('dt-cigar-shop').size()).toEqual(1);
            
            dirScope.shops = {1: {id: 1,
                                  name: 'i will be deleted'}};
            expect(dirScope.shops[1]).toBeDefined();
            dirScope.removeShop(1);
            parentScope.$digest();
            expect(dirScope.shops[1]).not.toBeDefined();
        });
    });
});