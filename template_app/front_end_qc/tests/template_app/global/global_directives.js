describe("tests for the global directives", function() {
    "use strict";
    beforeEach(module("template_app"));
    beforeEach(module('test_html_js'));
    var elm;
    var $rootScope;
    var $compile;
    var parentScope;
    var dirScope;
    var djangoLoginSpy = jasmine.createSpy('djangoLogin');
    var djangoLogoutSpy = jasmine.createSpy('djangoLogout');
    
    describe("tests for the user control panel header directive", function() {
        beforeEach(module(function($provide) {
            $provide.value("djangoLogin", djangoLoginSpy);
            $provide.value("djangoLogout", djangoLogoutSpy);
        }));
        
        beforeEach(inject(function(_$rootScope_, _$compile_) {
            elm = angular.element("<dt-user-cp-header diruser='theUser'></dt-user-cp-header>");
            $rootScope = _$rootScope_;
            $compile = _$compile_;
            parentScope = $rootScope.$new();
        }));
        
        it("fills out the dtUserCpHeader template with login stuff when diruser is falsy", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('div button').text()).toEqual('login');
            expect(dirScope.diruser).not.toBeDefined();
            expect(dirScope.info_holder).toBeDefined();
            expect(dirScope.info_holder.username).toEqual('');
            expect(dirScope.info_holder.password).toEqual('');
            expect(dirScope.django_login).toBeDefined();
            expect(dirScope.django_logout).toBeDefined();
        });
        
        it("fills out the dtUserCpHeader template with logout stuff when diruser is truthy", function() {
            parentScope.theUser = {'username': 'testing', 'email': 'testing@testing.com'};
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            expect(elm.find('div button').text()).toEqual('logout');
            expect(dirScope.diruser.username).toEqual('testing');
        });
        
        it("calls through to djangoLogin service when django_login is invoked", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            dirScope.django_login();
            expect(djangoLoginSpy).toHaveBeenCalledWith('', '', undefined);
        });
        
        it("calls through to djangoLogout service when django_logout is invoked", function() {
            $compile(elm)(parentScope);
            parentScope.$digest();
            dirScope = elm.isolateScope();
            dirScope.django_logout();
            expect(djangoLogoutSpy).toHaveBeenCalledWith(undefined);
        });
    });
});