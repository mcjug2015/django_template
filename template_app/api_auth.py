''' module for custom tastypie authorization '''
# pylint: disable=R0201
from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class UserObjectsAuthorization(Authorization):
    ''' Tastypie auth for the django User endpoint '''

    def read_list(self, object_list, bundle):
        ''' not allowed '''
        return object_list.filter(pk=bundle.request.user.pk)

    def read_detail(self, object_list, bundle):
        ''' can read any single object owned by them '''
        return bundle.obj.pk == bundle.request.user.pk

    def create_list(self, object_list, bundle):
        ''' not allowed '''
        raise Unauthorized('You may only grab the specific object for the user you are logged in as')

    def create_detail(self, object_list, bundle):
        ''' not allowed '''
        raise Unauthorized('You may only grab the specific object for the user you are logged in as')

    def update_list(self, object_list, bundle):
        ''' not allowed '''
        raise Unauthorized('You may only grab the specific object for the user you are logged in as')

    def update_detail(self, object_list, bundle):
        ''' not allowed '''
        raise Unauthorized('You may only grab the specific object for the user you are logged in as')

    def delete_list(self, object_list, bundle):
        ''' not allowed '''
        raise Unauthorized('You may only grab the specific object for the user you are logged in as')

    def delete_detail(self, object_list, bundle):
        ''' not allowed '''
        raise Unauthorized('You may only grab the specific object for the user you are logged in as')


class OwnerObjectsOnlyAuthorization(Authorization):
    ''' Tastypie authorization for objects with an owner field '''

    def _limit_qs(self, the_qs, user):
        ''' limit a queryset by owner '''
        return the_qs.filter(owner=user)

    def _limit_detail(self, the_obj, user):
        ''' limit an item by owner '''
        return the_obj.owner == user

    def _limit_list_unsaved(self, the_list, user):
        ''' limit a list of object by owner '''
        allowed = []
        # Since they may not all be saved, iterate over them.
        for obj in the_list:
            if obj.owner == user:
                allowed.append(obj)
        return allowed

    def read_list(self, object_list, bundle):
        ''' can read list of objects owned by them '''
        return self._limit_qs(object_list, bundle.request.user)

    def read_detail(self, object_list, bundle):
        ''' can read any single object owned by them '''
        return self._limit_detail(bundle.obj, bundle.request.user)

    def create_list(self, object_list, bundle):
        ''' only allowed to create list of objects for themselves '''
        return self._limit_list_unsaved(object_list, bundle.request.user)

    def create_detail(self, object_list, bundle):
        ''' only allowed to create individual objects for themselves '''
        return self._limit_detail(bundle.obj, bundle.request.user)

    def update_list(self, object_list, bundle):
        ''' only allowed to update objects they own '''
        return self._limit_list_unsaved(object_list, bundle.request.user)

    def update_detail(self, object_list, bundle):
        ''' can only update individual objects belonging to them '''
        return self._limit_detail(bundle.obj, bundle.request.user)

    def delete_list(self, object_list, bundle):
        ''' can only delete lists of objects they own '''
        return self._limit_qs(object_list, bundle.request.user)

    def delete_detail(self, object_list, bundle):
        ''' can only delete individual objects they own '''
        return self._limit_detail(bundle.obj, bundle.request.user)
